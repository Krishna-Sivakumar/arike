from django.db import models

LOCAL_BODY_CHOICES = (
    # Panchayath levels
    (1, "Grama Panchayath"),
    (2, "Block Panchayath"),
    (3, "District Panchayath"),
    (4, "Nagar Panchayath"),
    # Municipality levels
    (10, "Municipality"),
    # Corporation levels
    (20, "Corporation"),
    # Unknown
    (50, "Others"),
)

FACILITY_KIND_CHOICES = (
    ("PHC", "PHC"),
    ("CHC", "CHC")
)

GENDER_CHOICES = (
    ("MALE", "MALE"),
    ("FEMALE", "FEMALE"),
    ("OTHER", "OTHER")
)

FAMILY_RELATION_CHOICES = (
    ("PARENT", "PARENT"),
    ("CHILD", "CHILD"),
    ("RELATIVE", "RELATIVE"),
    ("NEIGHBOUR", "NEIGHBOUR"),
    ("FRIEND", "FRIEND"),
    ("NONE", "NONE")
)

TREATMENT_GROUPS = [
    ('General care', (
        ('MC', 'Mouth care'),
        ('BA', 'Bath'),
        ('NC', 'Nail cutting'),
        ('SH', 'Shaving')
    )),
    ('Genito urinary care', (
        ('PC', 'Perennial care'),
        ('CCT', 'Condom catheterisation & training'),
        ('NCT', 'Nelcath catheterisation & training'),
        ('FC', 'Foley’s catheterisation'),
        ('FCC', 'Foley’s catheter care'),
        ('SC', 'Suprapubic catheterisation'),
        ('SCC', 'Suprapubic catheter care'),
        ('BWN', 'Bladder wash with normal saline'),
        ('BWS', 'Bladder wash with soda bicarbonate'),
        ('UC', 'Urostomy care'),
    )),
    ('Gastro-intestinal care', (
        ('RTI', 'Ryles tube insertion'),
        ('RTC', 'Ryles tube care'),
        ('RTT', 'Ryles tube feeding & training'),
        ('PGC', 'PEG care'),
        ('PRE', 'Per Rectal Enema'),
        ('HE', 'High enema'),
        ('BS', 'Bisacodyl Suppository'),
        ('DE', 'Digital evacuation'),
        ('CC', 'Colostomy care'),
        ('CIC', 'Colostomy irrigation care'),
        ('IC', 'ileostomy care'),
    )),
    ('Wound care', (
        ('WCT', 'Wound care training given to family'),
        ('WD', 'Wound dressing'),
        ('SR', 'Suture removal'),
        ('VD', 'Vacuum dressing'),
    )),
    ('Respiratory care', (
        ('TC', 'Tracheostomy care'),
        ('CP', 'Chest physiotherapy'),
        ('IT', 'Inhaler training'),
        ('OCT', 'Oxygen concentrator - training'),
        ('BPT', 'Bi-PAP training'),
        ('BD', 'Bandaging'),
        ('ULLB', 'Upper limb lymphedema bandaging'),
        ('LLLB', 'Lower limb lymphedema bandaging'),
        ('ULLH', 'Upper limb lymphedema hosiery'),
        ('PVOD', 'PVOD bandaging'),
    )),
    ('Invasive care', (
        ('IFI', 'IV fluid infusion'),
        ('IMBA', 'IV medicine bolus administration'),
        ('ICC', 'IV cannula care'),
        ('ICI', 'IV cannula insertion'),
        ('SCI', 'S/C cannula insertion'),
        ('SCIS', 'S/C fluid infusion (subcutaneous)'),
        ('SMBA', 'S/C medicine bolus administration'),
        ('SCCC', 'S/C cannula care'),
        ('AT', 'Ascites tapping'),
        ('ACC', 'Ascitic catheter care'),
    )),
    ('Physiotherapy', (
        ('PM', 'Passive Movement'),
        ('AM', 'Active Movement'),
        ('SE', 'Strengthening exercises'),
        ('NDT', 'NDT'),
        ('GAIT', 'GAIT Training'),
        ('MTT', 'Modalities + text field'),
        ('BE', 'Breathing exercises'),
        ('BCE', 'Balance & Coordination exercises'),
        ('ST', 'Stretching'),
        ('PCR', 'Postural correction'),
    )),
]

SYMPTOM_CHOICES = [
    (1, "ASYMPTOMATIC"),
    (2, "FEVER"),
    (3, "SORE THROAT"),
    (4, "COUGH"),
    (5, "BREATHLESSNESS"),
    (6, "MYALGIA"),
    (7, "ABDOMINAL DISCOMFORT"),
    (8, "VOMITING/DIARRHOEA"),
    (9, "OTHERS"),
    (10, "SARI"),
    (11, "SPUTUM"),
    (12, "NAUSEA"),
    (13, "CHEST PAIN"),
    (14, "HEMOPTYSIS"),
    (15, "NASAL DISCHARGE"),
    (16, "BODY ACHE"),
]


# Abstract Classes


class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        field_names = [field.name for field in self._meta.get_fields()]
        if "name" in field_names:
            return self.name
        elif "full_name" in field_names:
            return self.full_name
        return f"{self.__class__.__name__}.{self.pk}"

    class Meta:
        abstract = True
