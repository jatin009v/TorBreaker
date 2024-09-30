from django.db import models

class Pipeline(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'low'),
        ('medium', 'medium'),
        ('high', 'high'),
        ('critical', 'critical'),
    ]
    
    name = models.CharField(max_length=100, default='')
    sequenceno = models.IntegerField(default=1) 
    cmd =models.TextField(default='') 
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='low')

    def __str__(self):
        return self.name.upper()

class ActiveScan(models.Model):
    user   = models.CharField(max_length=100, default='cybersage')
    domain = models.CharField(max_length=255, default='testphp.vulnweb.com')
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.domain + " " + f"[Vulnerability: {self.pipeline.name}]" + f" [Completed: {self.is_completed}]"

class NetworkScan(models.Model):
    user   = models.CharField(max_length=100, default='cybersage')
    domain = models.CharField(max_length=255, default='testphp.vulnweb.com')
    SoftwareName = models.CharField(max_length=100, default='')
    CVE         = models.CharField(max_length=100, default='')
    Description = models.TextField(default='')
    MaxCVSS     = models.CharField(max_length=100, default='')
    EPSS_Score  = models.CharField(max_length=100, default='')
    Published   = models.CharField(max_length=100, default='')
    Updated     = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.domain + " " + f"[CVE: {self.CVE}]"

class WhiteBoxResult(models.Model):
    user   = models.CharField(max_length=100, default='cybersage')
    domain = models.CharField(max_length=255, default='testphp.vulnweb.com')
    VulnerabilityName = models.CharField(max_length=100, default='')
    VulnerableFilePath = models.CharField(max_length=100, default='')
    VulnerabilityDescription = models.TextField(default='')
    Message     = models.CharField(max_length=100, default='')
    StartLine  = models.CharField(max_length=100, default='')
    EndLine   = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.domain + " " + f"[{self.VulnerabilityName}]"

class Fingerprint(models.Model):
    user      = models.CharField(max_length=100, default='cybersage')
    domain    = models.CharField(max_length=255, default='testphp.vulnweb.com')
    tech_list = models.JSONField()
    waf_info  = models.TextField()

    def __str__(self):
        return self.domain + " " + f"[{self.domain}]" + f" [User: {self.user}]"

class Result(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'low'),
        ('medium', 'medium'),
        ('high', 'high'),
        ('critical', 'critical'),
    ]

    user = models.CharField(max_length=100, default='cybersage')
    vulnerability_type = models.CharField(max_length=100 , default='')
    is_vulnerable = models.BooleanField(default=False)
    payload= models.TextField(default='')
    endpoint= models.CharField(max_length=100 , default='')
    url = models.CharField(max_length=255 , default='')
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='low')
    website = models.TextField(default='testphp.vulnweb.com')

    def __str__(self):
        return f"[{self.vulnerability_type}] [{self.url}]"