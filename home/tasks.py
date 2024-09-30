from celery import shared_task
from home.FingerprintEnum import FingerprintEnum
from home.Recon import Recon 
from home.Scanner import Scanner
from home.CVESearch import CVESearch
from home.models import Pipeline
from home.models import Result
from home.models import ActiveScan
from home.models import Fingerprint
from home.models import NetworkScan
from home.models import WhiteBoxResult
from home.CodeFixer import CodeFixer

@shared_task
def codefixer_task(github_repo):
    fixed = CodeFixer()
    fixed.start(github_repo)

@shared_task(bind=True)
def web_scanner(self, current_user, domain, pipeline_list):
    output_log = ""

    def printer(new_output_log):
        nonlocal output_log
        output_log += new_output_log + "\n"
        print(new_output_log)
        self.update_state(state='PROGRESS', meta={'output_log': output_log})

    # Code expects full URL with HTTP/HTTPS Schema
    printer("[*] Performing Fingerprinting on Target ...")    
    fingerprinting = FingerprintEnum()
    tech_list, waf_info, only_domain = fingerprinting.start(domain)
    fingerprint, created = Fingerprint.objects.get_or_create(user=current_user, domain=only_domain, defaults={'tech_list': tech_list, 'waf_info': waf_info})

    if not created:
        fingerprint.tech_list = tech_list
        fingerprint.waf_info = waf_info
        fingerprint.save()
    printer("[+] Fingerprint Completed")

    # Delete Previous Scan Report
    NetworkScan.objects.filter(domain=only_domain).delete()
    Result.objects.filter(website=only_domain).delete()
    WhiteBoxResult.objects.filter(domain=only_domain).delete()

    printer("[*] Performing Network Vulnerability Audit ...")
    for key,value in tech_list.items():
        if len(value["versions"]) != 0:
            search_query = key +" "+ value['versions'][0]
            scraper = CVESearch(search_query)
            scraped_data = scraper.start()

            for data in scraped_data:
                NetworkScan.objects.create(user=current_user,
                                           domain=only_domain,
                                           SoftwareName = data['Software'],
                                           CVE         = data['CVE'],
                                           Description = data['Description'],
                                           MaxCVSS     = data['Max CVSS'],
                                           EPSS_Score  = data['EPSS Score'],
                                           Published   = data['Published'],
                                           Updated     = data['Updated'])
    printer("[+] Completed Network Audit")

    # print("[*] Performing WhiteBox Pentesting ...")

    # print("[+] Completed WhiteBox")

    printer("[*] Performing Reconnaissance ...")
    recon = Recon()
    get_params_path, post_params_path, random_suffix = recon.url_recon(domain)
    printer(f"[+] Get URLs: {get_params_path}")
    printer(f"[+] POST URLs: {post_params_path}")
    printer("[+] Completed Recon")

    printer("[*] Performing Vulnerability Scanning ...")
    scanner_web = Scanner()
    for pipeline_name in pipeline_list:
        printer(f"[*] Testing Vulnerability: {pipeline_name}")
        try:
            cmd_list = {}
            cmds = Pipeline.objects.filter(name=pipeline_name)
            vuln_severity = cmds.first().severity
            for data in cmds:
                cmd_list[data.sequenceno] = data.cmd

            sorted_cmd_list = [value for key, value in sorted(cmd_list.items(), key=lambda x: x[0])]
            get_result, post_result = scanner_web.start(domain, only_domain, vuln_severity, random_suffix, pipeline_name, sorted_cmd_list, get_params_path, post_params_path)
            for data in get_result:
                Result.objects.create(vulnerability_type=data['vulnerability_type'], 
                                    is_vulnerable=data['is_vulnerable'],
                                    payload=data['payload'],
                                    endpoint=data['endpoint'],
                                    url=data['url'],
                                    severity=data['severity'],
                                    user=current_user,
                                    website=only_domain,
                                    )
            for data in post_result:
                Result.objects.create(vulnerability_type=data['vulnerability_type'], 
                                    is_vulnerable=data['is_vulnerable'],
                                    payload=data['payload'],
                                    endpoint=data['endpoint'],
                                    url=data['url'],
                                    severity=data['severity'],
                                    user=current_user,
                                    website=only_domain,
                                    )
            printer(f"[+] Completed {pipeline_name} scan")
        except Exception as e: 
            printer(f"Error: {e}") 
            
        ActiveScan.objects.filter(user=current_user, domain=domain, pipeline__name=pipeline_name).update(is_completed=True)
    ActiveScan.objects.filter(user=current_user, domain=domain, pipeline__name__in=pipeline_list).delete()
    return True  