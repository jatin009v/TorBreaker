from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Pipeline, ActiveScan, Result, Fingerprint, NetworkScan
from .tasks import web_scanner, codefixer_task
from django.http import JsonResponse

@login_required
def scan_page(request):
    if request.method == 'POST':
        domain = request.POST.get('domain')
        selected_pipelines = request.POST.getlist('pipelines')
        pipeline_names_list = []
        for pipeline_id in selected_pipelines:
            pipeline = Pipeline.objects.get(id=pipeline_id)
            pipeline_names_list.append(pipeline.name)
            ActiveScan.objects.create(user=request.user.username, domain=domain, pipeline=pipeline)

        # task_result = web_scanner.delay(request.user.username, domain, pipeline_names_list)
        task_result = web_scanner.apply_async(args=[request.user.username, domain, pipeline_names_list])

        task_id = task_result.id

        # Redirect to the waiting page with the task ID
        return redirect('progress', task_id=task_id)
    
    pipelines = Pipeline.objects.all().distinct()
    context = {'pipelines': pipelines}
    return render(request, 'scan.html', context)

@login_required
def progress(request, task_id=None):
    scan_progress = ActiveScan.objects.filter(user=request.user)
    context = {'scan_progress': scan_progress, 'task_id': task_id}
    return render(request, "progress.html", context)

@login_required
def browse_result(request):
    results = Result.objects.all().distinct().values_list("website", flat=True)
    context = {'results': results}
    return render(request, "browse_result.html", context)

@login_required
def fix_code(request):
    task_result = codefixer_task.delay("https://github.com/PriyadarshiIndia/TestingWebsite")
    task_id = task_result.id 
    # task_id = ""
    context = {"task_id": task_id}
    return render(request, "codefixer_wait.html", context)

@login_required
def result(request, website):
    scan_result = Result.objects.filter(user=request.user, website=website)
    
    try:
        fingerprint_result = Fingerprint.objects.filter(user=request.user, domain=website).first()
        tech_list = fingerprint_result.tech_list
        waf_info  = fingerprint_result.waf_info
    except Exception as e:
        tech_list = {}
        waf_info = "No Web Application Firewall (WAF) Detected"

    # CVE Search
    network_result = NetworkScan.objects.filter(user=request.user, domain=website)
    
    # Preprocess counts for each severity level
    low_severity_count = scan_result.filter(severity='low').count()
    medium_severity_count = scan_result.filter(severity='medium').count()
    high_severity_count = scan_result.filter(severity='high').count()
    critical_severity_count = scan_result.filter(severity='critical').count()
    vulnerable_urls_count = scan_result.filter(is_vulnerable=True).count()

    context = {
        'tech_list': tech_list,
        'waf_info': waf_info,
        'network_result': network_result,
        'scan_result': scan_result,
        'low_severity_count': low_severity_count,
        'medium_severity_count': medium_severity_count,
        'high_severity_count': high_severity_count,
        'critical_severity_count': critical_severity_count,
        'vulnerable_urls_count': vulnerable_urls_count,
    }

    return render(request, "result.html", context)


 

