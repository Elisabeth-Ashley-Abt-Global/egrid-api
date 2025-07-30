from django.db import models

 
class BalancingAuthority(models.Model): 
    bacode = models.CharField(max_length=20, primary_key=True, unique=True)  
    baname = models.CharField(max_length=255)   
    banamepcap = models.FloatField(null=True, blank=True)
  
    class Meta:
        db_table = "balancing_authority"

    def __str__(self):
        return self.name

# Make bacode a FK
class Plant(models.Model):
    seqplt   = models.IntegerField(null=True, blank=True) # seqplt
    orispl   = models.IntegerField(null=False, blank=False, unique=True)  # Plant ID ADD A UNIQUE CONSTRAINT
    pstatabb = models.CharField(max_length=1000, null=True, blank=True)
    fipsst   = models.CharField(max_length=2, null=True, blank=True)  # State Id
    pname    = models.CharField(max_length=1000, null=True, blank=True)
    oprcode  = models.IntegerField(null=True, blank=True)
    utlsrvid = models.IntegerField(null=True, blank=True)
    sector   = models.CharField(max_length=1000, null=True, blank=True)
    # bacode   = models.CharField(max_length=1000, null=True, blank=True)
    bacode = models.ForeignKey(
        BalancingAuthority,
        to_field='bacode',
        on_delete=models.CASCADE,  
        db_column='bacode'          
    )   
    nerc     = models.CharField(max_length=1000, null=True, blank=True)
    fipscnty = models.CharField(max_length=3, null=True, blank=True)
    lat      = models.FloatField(null=True, blank=True)
    lon      = models.FloatField(null=True, blank=True)
    numunt   = models.IntegerField(null=True, blank=True)
    numgen   = models.IntegerField(null=True, blank=True)
    plprmfl  = models.CharField(max_length=1000, null=True, blank=True)
    plfuelct = models.CharField(max_length=1000, null=True, blank=True)
    coalflag = models.CharField(max_length=1000, null=True, blank=True)
    subrgn   = models.CharField(null=True, blank=True, max_length=4) 
    isorto   = models.CharField(null=True, blank=True, max_length=5)
    namepcap = models.FloatField(null=True, blank=True)
    cntyname = models.CharField(max_length=4000, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'plant'


class BaAdjustedValues(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    bacode = models.ForeignKey(
        BalancingAuthority, 
        on_delete=models.CASCADE, # Deletes BaAdjustedValues records if the related BalancingAuthority is delet
        db_column='bacode',
        to_field='bacode'
    )
    banamepcap = models.FloatField(null=True, blank=True)
    bahtian    = models.FloatField(null=True, blank=True, db_comment='BA annual heat input from combustion (MMBtu)')  # BA annual heat input (MMBtu)
    bahtioz    = models.FloatField(null=True, blank=True)
    bahtiant   = models.FloatField(null=True, blank=True)
    bahtiozt   = models.FloatField(null=True, blank=True)
    bangenan   = models.FloatField(null=True, blank=True)
    bangenoz   = models.FloatField(null=True, blank=True)
    bangennb   = models.FloatField(null=True, blank=True)
    banoxan    = models.FloatField(null=True, blank=True)
    banoxoz    = models.FloatField(null=True, blank=True)
    baso2an    = models.FloatField(null=True, blank=True)
    baco2an    = models.FloatField(null=True, blank=True)
    bach4an    = models.FloatField(null=True, blank=True)
    ban2oan    = models.FloatField(null=True, blank=True)
    baco2eqa   = models.FloatField(null=True, blank=True)
    bahgan     = models.FloatField(null=True, blank=True)  
    # created_on = models.DateTimeField(auto_now_add=True)  # Automatically sets the field to the current timestamp only when the record is first created.
    # updated_on = models.DateTimeField(auto_now=True) # Automatically updates the field to the current timestamp every time the record is saved.
    year = models.IntegerField(null=True, blank=True)  # Year
 
    class Meta:
        db_table = "ba_adjusted_values"
        constraints = [
            models.UniqueConstraint(fields=["bacode", "year"], name="bav_unique_bacode_year")
        ]

    def __str__(self):
        return self.name
 
class BaEmissionRate(models.Model):
    id     =  models.AutoField(primary_key=True) 
    bacode = models.ForeignKey(
        BalancingAuthority,
        on_delete=models.CASCADE,  # Deletes BaEmissionRate records if the related BalancingAuthority is deleted
        db_column='bacode',          # Ensures the column in the database is still named 'bacode'
        to_field='bacode' 
    )
    banoxrta = models.FloatField(null=True, blank=True)
    banoxrto = models.FloatField(null=True, blank=True)
    baso2rta = models.FloatField(null=True, blank=True)
    baco2rta = models.FloatField(null=True, blank=True)
    bach4rta = models.FloatField(null=True, blank=True)
    ban2orta = models.FloatField(null=True, blank=True)
    bac2erta = models.FloatField(null=True, blank=True)
    bahgrta  = models.CharField(null=True, blank=True)
    banoxra  = models.FloatField(null=True, blank=True)
    banoxro  = models.FloatField(null=True, blank=True)
    baso2ra  = models.FloatField(null=True, blank=True)
    baco2ra  = models.FloatField(null=True, blank=True)
    bach4ra  = models.FloatField(null=True, blank=True)
    ban2ora  = models.FloatField(null=True, blank=True)
    bac2era  = models.FloatField(null=True, blank=True)
    bahgra   = models.CharField(null=True, blank=True)
    banoxcrt = models.FloatField(null=True, blank=True)
    banoxcro = models.FloatField(null=True, blank=True)
    baso2crt = models.FloatField(null=True, blank=True)
    baco2crt = models.FloatField(null=True, blank=True)
    bach4crt = models.FloatField(null=True, blank=True)
    ban2ocrt = models.FloatField(null=True, blank=True)
    bac2ecrt = models.FloatField(null=True, blank=True)
    bahgcrt  = models.CharField(null=True, blank=True)
    # created_on = models.DateTimeField(auto_now_add=True)  # Automatically sets the field to the current timestamp only when the record is first created.
    # updated_on = models.DateTimeField(auto_now=True) # Automatically updates the field to the current timestamp every time the record is saved.
    year = models.IntegerField(null=True, blank=True)  # Year
 
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ba_emission_rate'
        constraints = [
            models.UniqueConstraint(fields=["bacode", "year"], name="ba_emission_rate_unique_bacode_year")
        ]

class BaFuelTypeEmissionRate(models.Model):
    id       =  models.AutoField(primary_key=True) 
    bacode = models.ForeignKey(
        BalancingAuthority,
        on_delete=models.CASCADE,   # Deletes BaFuelTypeEmissionRate records if the related BalancingAuthority is deleted
        db_column='bacode',          # Ensures the column in the database is still named 'ba_id'
        to_field='bacode'
    )
    bacnoxrt  = models.FloatField(blank=True, null=True)
    baonoxrt  = models.FloatField(blank=True, null=True)
    bagnoxrt  = models.FloatField(blank=True, null=True)
    bafsnxrt  = models.FloatField(blank=True, null=True)
    bacnxort  = models.FloatField(blank=True, null=True)
    baonxort  = models.FloatField(blank=True, null=True)
    bagnxort  = models.FloatField(blank=True, null=True)
    bafsnort  = models.FloatField(blank=True, null=True)
    bacso2rt  = models.FloatField(blank=True, null=True)
    baoso2rt  = models.FloatField(blank=True, null=True)
    bagso2rt  = models.FloatField(blank=True, null=True)
    bafss2rt  = models.FloatField(blank=True, null=True)
    bacco2rt  = models.FloatField(blank=True, null=True)
    baoco2rt  = models.FloatField(blank=True, null=True)
    bagco2rt  = models.FloatField(blank=True, null=True)
    bafsc2rt  = models.FloatField(blank=True, null=True)
    bacch4rt  = models.FloatField(blank=True, null=True)
    baoch4rt  = models.FloatField(blank=True, null=True)
    bagch4rt  = models.FloatField(blank=True, null=True)
    bafch4rt  = models.FloatField(blank=True, null=True)
    bacn2ort  = models.FloatField(blank=True, null=True)
    baon2ort  = models.FloatField(blank=True, null=True)
    bagn2ort  = models.FloatField(blank=True, null=True)
    bafn2ort  = models.FloatField(blank=True, null=True)
    bacc2ert  = models.FloatField(blank=True, null=True)
    baoc2ert  = models.FloatField(blank=True, null=True)
    bagc2ert  = models.FloatField(blank=True, null=True)
    bafsc2ert = models.FloatField(blank=True, null=True)
    bachgrt   = models.CharField(max_length=2, blank=True, null=True) 
    bafshgrt  = models.CharField(max_length=2, blank=True, null=True) 
    bacnoxr   = models.FloatField(blank=True, null=True)
    baonoxr   = models.FloatField(blank=True, null=True)
    bagnoxr   = models.FloatField(blank=True, null=True)
    bafsnxr   = models.FloatField(blank=True, null=True)
    bacnxor   = models.FloatField(blank=True, null=True)
    baonxor   = models.FloatField(blank=True, null=True)
    bagnxor   = models.FloatField(blank=True, null=True)
    bafsnor   = models.FloatField(blank=True, null=True)
    bacso2r   = models.FloatField(blank=True, null=True)
    baoso2r   = models.FloatField(blank=True, null=True)
    bagso2r   = models.FloatField(blank=True, null=True)
    bafss2r   = models.FloatField(blank=True, null=True)
    bacco2r   = models.FloatField(blank=True, null=True)
    baoco2r   = models.FloatField(blank=True, null=True)
    bagco2r   = models.FloatField(blank=True, null=True)
    bafsc2r   = models.FloatField(blank=True, null=True)
    bacch4r   = models.FloatField(blank=True, null=True)
    baoch4r   = models.FloatField(blank=True, null=True)
    bagch4r   = models.FloatField(blank=True, null=True)
    bafch4r   = models.FloatField(blank=True, null=True)
    bacn2or   = models.FloatField(blank=True, null=True)
    baon2or   = models.FloatField(blank=True, null=True)
    bagn2or   = models.FloatField(blank=True, null=True)
    bafn2or   = models.FloatField(blank=True, null=True)
    bacc2er   = models.FloatField(blank=True, null=True)
    baoc2er   = models.FloatField(blank=True, null=True)
    bagc2er   = models.FloatField(blank=True, null=True)
    bafsc2er  = models.FloatField(blank=True, null=True)
    bachgr    = models.CharField(max_length=2, blank=True, null=True)
    bafshgr   = models.CharField(max_length=2, blank=True, null=True) 
    year      = models.IntegerField(null=True, blank=True)   
 
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ba_fuel_type_emission_rate'
        constraints = [
            models.UniqueConstraint(fields=["bacode", "year"], name="ba_fuel_type_emission_rate_unique_bacode_year")
        ]
 
class BaFuelTypeGeneration(models.Model):
    id =  models.AutoField(primary_key=True) 
    bacode = models.ForeignKey(
        BalancingAuthority,
        on_delete=models.CASCADE,   # Deletes BaFuelTypeGeneration records if the related BalancingAuthority is deleted
        db_column='bacode',          # Ensures the column in the database is still named 'ba_id'
        to_field='bacode'
    )
    bagenacl = models.FloatField(blank=True, null=True)
    bagenaol = models.FloatField(blank=True, null=True)
    bagenags = models.FloatField(blank=True, null=True)
    bagenanc = models.FloatField(blank=True, null=True)
    bagenahy = models.FloatField(blank=True, null=True)
    bagenabm = models.FloatField(blank=True, null=True)
    bagenawi = models.FloatField(blank=True, null=True)
    bagenaso = models.FloatField(blank=True, null=True)
    bagenagt = models.FloatField(blank=True, null=True)
    bagenaof = models.FloatField(blank=True, null=True)
    bagenaop = models.FloatField(blank=True, null=True)
    bagenatn = models.FloatField(blank=True, null=True)
    bagenatr = models.FloatField(blank=True, null=True)
    bagenato = models.FloatField(blank=True, null=True)
    bagenath = models.FloatField(blank=True, null=True)
    bagenacy = models.FloatField(blank=True, null=True)
    bagenacn = models.FloatField(blank=True, null=True)
    bagenaco = models.FloatField(blank=True, null=True)
    year = models.IntegerField(null=True, blank=True)  

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ba_fuel_type_generation'
        constraints = [
            models.UniqueConstraint(fields=["bacode", "year"], name="ba_fuel_type_gen_unique_bacode_year")
        ]


class BaNonBaseloadValues(models.Model):
    id       =  models.AutoField(primary_key=True) 
    bacode = models.ForeignKey(
        BalancingAuthority,
        on_delete=models.CASCADE,   # Deletes BaNonBaseloadValues records if the related BalancingAuthority is deleted
        db_column='bacode',          # Ensures the column in the database is still named 'ba_id'
        to_field='bacode'
    )
    banbnox  = models.FloatField(null=True, blank=True)
    banbnxo  = models.FloatField(null=True, blank=True)
    banbso2  = models.FloatField(null=True, blank=True)
    banbco2  = models.FloatField(null=True, blank=True)
    banbch4  = models.FloatField(null=True, blank=True)
    banbn2o  = models.FloatField(null=True, blank=True)
    banbc2e  = models.FloatField(null=True, blank=True)
    banbhg   = models.CharField(max_length=2, null=True, blank=True)
    banbgncl = models.FloatField(null=True, blank=True)
    banbgnol = models.FloatField(null=True, blank=True)
    banbgngs = models.FloatField(null=True, blank=True)
    banbgnnc = models.FloatField(null=True, blank=True)
    banbgnhy = models.FloatField(null=True, blank=True)
    banbgnbm = models.FloatField(null=True, blank=True)
    banbgnwi = models.FloatField(null=True, blank=True)
    banbgnso = models.FloatField(null=True, blank=True)
    banbgngt = models.FloatField(null=True, blank=True)
    banbgnof = models.FloatField(null=True, blank=True)
    banbgnop = models.FloatField(null=True, blank=True)
    banbclpr = models.FloatField(null=True, blank=True)
    banbolpr = models.FloatField(null=True, blank=True)
    banbgspr = models.FloatField(null=True, blank=True)
    banbncpr = models.FloatField(null=True, blank=True)
    banbhypr = models.FloatField(null=True, blank=True)
    banbbmpr = models.FloatField(null=True, blank=True)
    banbwipr = models.FloatField(null=True, blank=True)
    banbsopr = models.FloatField(null=True, blank=True)
    banbgtpr = models.FloatField(null=True, blank=True)
    banbofpr = models.FloatField(null=True, blank=True)
    banboppr = models.FloatField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)   
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ba_nonbaseload_values'
        constraints = [
            models.UniqueConstraint(fields=["bacode", "year"], name="ba_nonbaseload_values_unique_bacode_year")
        ]


class BaResourceMix(models.Model):
    id       =  models.AutoField(primary_key=True) 
    bacode = models.ForeignKey(
        BalancingAuthority,
        on_delete=models.CASCADE,   # Deletes BaResourceMix records if the related BalancingAuthority is deleted
        db_column='bacode',          # Ensures the column in the database is still named 'bacode'
        to_field='bacode'
    )
    baclpr = models.FloatField(blank=True, null=True)
    baolpr = models.FloatField(blank=True, null=True)
    bagspr = models.FloatField(blank=True, null=True)
    bancpr = models.FloatField(blank=True, null=True)
    bahypr = models.FloatField(blank=True, null=True)
    babmpr = models.FloatField(blank=True, null=True)
    bawipr = models.FloatField(blank=True, null=True)
    basopr = models.FloatField(blank=True, null=True)
    bagtpr = models.FloatField(blank=True, null=True)
    baofpr = models.FloatField(blank=True, null=True)
    baoppr = models.FloatField(blank=True, null=True)
    batnpr = models.FloatField(blank=True, null=True)
    batrpr = models.FloatField(blank=True, null=True)
    batopr = models.FloatField(blank=True, null=True)
    bathpr = models.FloatField(blank=True, null=True)
    bacypr = models.FloatField(blank=True, null=True)
    bacnpr = models.FloatField(blank=True, null=True)
    bacopr = models.FloatField(blank=True, null=True)
    year = models.IntegerField(null=True, blank=True)  

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ba_resource_mix'
        constraints = [
            models.UniqueConstraint(fields=["bacode", "year"], name="ba_resource_mix_unique_bacode_year")
        ]

class Generator(models.Model):
    seqgen = models.FloatField(null=True, blank=True) 
    genid = models.CharField(null=True, blank=True)  
    orispl = models.IntegerField(null=False, blank=False)  
 
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'generator'

        constraints = [
            models.UniqueConstraint(fields=['genid', 'orispl'], name='unique_genid_orispl')
        ]


class Generation(models.Model): 
    genid = models.CharField(null=True, blank=True)  
    orispl = models.IntegerField(null=False, blank=False)  
    numblr   = models.IntegerField(null=True, blank=True)
    genstat  = models.CharField(max_length=500, null=True, blank=True)
    prmvr    = models.CharField(max_length=500, null=True, blank=True)
    fuelg1   = models.CharField(max_length=500, null=True, blank=True)
    namepcap = models.FloatField(null=True, blank=True)
    cfact    = models.FloatField(null=True, blank=True)
    genntan  = models.FloatField(null=True, blank=True)
    genntoz  = models.FloatField(null=True, blank=True)
    genersrc = models.CharField(max_length=500, null=True, blank=True)
    genyronl = models.IntegerField(null=True, blank=True)
    genyrret = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)  # Year

    class Meta:
        db_table = 'generation'    

        constraints = [
            models.UniqueConstraint(fields=['genid', 'orispl', 'year'], name='unique_genid_orispl_year')
        ]
    

class NercRegion(models.Model):
    nerc = models.CharField(max_length=5, null=False, blank=False, unique=True)
    nercname = models.CharField(max_length=500, null=False, blank=False)
    nrnamepcap = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'nerc_region'


class NercAdjustedValues(models.Model): 
    id = models.AutoField(primary_key=True)
    nerc = models.ForeignKey(
                NercRegion,
                to_field='nerc',
                on_delete=models.CASCADE,  # Deletes NercAdjustedValues records if the related Plant is deleted
                db_column='nerc'          
            ) 
    nrnamepcap = models.FloatField(null=True, blank=True)
    nrhtian    = models.FloatField(null=True, blank=True)
    nrhtioz    = models.FloatField(null=True, blank=True)
    nrhtiant   = models.FloatField(null=True, blank=True)
    nrhtiozt   = models.FloatField(null=True, blank=True)
    nrngenan   = models.FloatField(null=True, blank=True)
    nrngenoz   = models.FloatField(null=True, blank=True)
    nrngennb   = models.FloatField(null=True, blank=True)
    nrnoxan    = models.FloatField(null=True, blank=True)
    nrnoxoz    = models.FloatField(null=True, blank=True)
    nrso2an    = models.FloatField(null=True, blank=True)
    nrco2an    = models.FloatField(null=True, blank=True)
    nrch4an    = models.FloatField(null=True, blank=True)
    nrn2oan    = models.FloatField(null=True, blank=True)
    nrco2eqa   = models.FloatField(null=True, blank=True)
    nrhgan     = models.CharField(max_length=2, null=True, blank=True) 
    year       = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'nerc_adjusted_values'
        constraints = [
            models.UniqueConstraint(fields=["nerc", "year"], name="nerc_adjusted_values_unique_nerc_year")
        ]


class NercEmissionRate(models.Model): 
    id = models.AutoField(primary_key=True)
    nerc = models.ForeignKey(
                NercRegion,
                to_field='nerc',
                on_delete=models.CASCADE,  # Deletes NercEmissionRate records if the related Plant is deleted
                db_column='nerc'          
            ) 
    nrnoxrta = models.FloatField(blank=True, null=True)
    nrnoxrto = models.FloatField(blank=True, null=True)
    nrso2rta = models.FloatField(blank=True, null=True)
    nrco2rta = models.FloatField(blank=True, null=True)
    nrch4rta = models.FloatField(blank=True, null=True)
    nrn2orta = models.FloatField(blank=True, null=True)
    nrc2erta = models.FloatField(blank=True, null=True)
    nrhgrta  = models.CharField(max_length=2, blank=True, null=True)
    nrnoxra  = models.FloatField(blank=True, null=True)
    nrnoxro  = models.FloatField(blank=True, null=True)
    nrso2ra  = models.FloatField(blank=True, null=True)
    nrco2ra  = models.FloatField(blank=True, null=True)
    nrch4ra  = models.FloatField(blank=True, null=True)
    nrn2ora  = models.FloatField(blank=True, null=True)
    nrc2era  = models.FloatField(blank=True, null=True)
    nrhgra   = models.CharField(max_length=2, blank=True, null=True)
    nrnoxcrt = models.FloatField(blank=True, null=True)
    nrnoxcro = models.FloatField(blank=True, null=True)
    nrso2crt = models.FloatField(blank=True, null=True)
    nrco2crt = models.FloatField(blank=True, null=True)
    nrch4crt = models.FloatField(blank=True, null=True)
    nrn2ocrt = models.FloatField(blank=True, null=True)
    nrc2ecrt = models.FloatField(blank=True, null=True)
    nrhgcrt  = models.CharField(max_length=2, blank=True, null=True)
    year     = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'nerc_emission_rate'
        constraints = [
            models.UniqueConstraint(fields=["nerc", "year"], name="nerc_emission_rate_unique_nerc_year")
        ]
  

class NercFuelTypeEmissionRate(models.Model):  
    id = models.AutoField(primary_key=True)
    nerc = models.ForeignKey(
                NercRegion,
                to_field='nerc',
                on_delete=models.CASCADE,  # Deletes NercFuelTypeEmissionRate records if the related Plant is deleted
                db_column='nerc'          
            ) 
    nrcnoxrt  = models.FloatField(blank=True, null=True)
    nronoxrt  = models.FloatField(blank=True, null=True)
    nrgnoxrt  = models.FloatField(blank=True, null=True)
    nrfsnxrt  = models.FloatField(blank=True, null=True)
    nrcnxort  = models.FloatField(blank=True, null=True)
    nronxort  = models.FloatField(blank=True, null=True)
    nrgnxort  = models.FloatField(blank=True, null=True)
    nrfsnort  = models.FloatField(blank=True, null=True)
    nrcso2rt  = models.FloatField(blank=True, null=True)
    nroso2rt  = models.FloatField(blank=True, null=True)
    nrgso2rt  = models.FloatField(blank=True, null=True)
    nrfss2rt  = models.FloatField(blank=True, null=True)
    nrcco2rt  = models.FloatField(blank=True, null=True)
    nroco2rt  = models.FloatField(blank=True, null=True)
    nrgco2rt  = models.FloatField(blank=True, null=True)
    nrfsc2rt  = models.FloatField(blank=True, null=True)
    nrcch4rt  = models.FloatField(blank=True, null=True)
    nroch4rt  = models.FloatField(blank=True, null=True)
    nrgch4rt  = models.FloatField(blank=True, null=True)
    nrfch4rt  = models.FloatField(blank=True, null=True)
    nrcn2ort  = models.FloatField(blank=True, null=True)
    nron2ort  = models.FloatField(blank=True, null=True)
    nrgn2ort  = models.FloatField(blank=True, null=True)
    nrfn2ort  = models.FloatField(blank=True, null=True)
    nrcc2ert  = models.FloatField(blank=True, null=True)
    nroc2ert  = models.FloatField(blank=True, null=True)
    nrgc2ert  = models.FloatField(blank=True, null=True)
    nrfsc2ert = models.FloatField(blank=True, null=True)
    nrchgrt   = models.CharField(max_length=2, blank=True, null=True)
    nrfshgrt  = models.CharField(max_length=2, blank=True, null=True)
    nrcnoxr   = models.FloatField(blank=True, null=True)
    nronoxr   = models.FloatField(blank=True, null=True)
    nrgnoxr   = models.FloatField(blank=True, null=True)
    nrfsnxr   = models.FloatField(blank=True, null=True)
    nrcnxor   = models.FloatField(blank=True, null=True)
    nronxor   = models.FloatField(blank=True, null=True)
    nrgnxor   = models.FloatField(blank=True, null=True)
    nrfsnor   = models.FloatField(blank=True, null=True)
    nrcso2r   = models.FloatField(blank=True, null=True)
    nroso2r   = models.FloatField(blank=True, null=True)
    nrgso2r   = models.FloatField(blank=True, null=True)
    nrfss2r   = models.FloatField(blank=True, null=True)
    nrcco2r   = models.FloatField(blank=True, null=True)
    nroco2r   = models.FloatField(blank=True, null=True)
    nrgco2r   = models.FloatField(blank=True, null=True)
    nrfsc2r   = models.FloatField(blank=True, null=True)
    nrcch4r   = models.FloatField(blank=True, null=True)
    nroch4r   = models.FloatField(blank=True, null=True)
    nrgch4r   = models.FloatField(blank=True, null=True)
    nrfch4r   = models.FloatField(blank=True, null=True)
    nrcn2or   = models.FloatField(blank=True, null=True)
    nron2or   = models.FloatField(blank=True, null=True)
    nrgn2or   = models.FloatField(blank=True, null=True)
    nrfn2or   = models.FloatField(blank=True, null=True)
    nrcc2er   = models.FloatField(blank=True, null=True)
    nroc2er   = models.FloatField(blank=True, null=True)
    nrgc2er   = models.FloatField(blank=True, null=True)
    nrfsc2er  = models.FloatField(blank=True, null=True)
    nrchgr    = models.CharField(max_length=2, blank=True, null=True)
    nrfshgr   = models.CharField(max_length=2, blank=True, null=True)
    year      = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'nerc_fuel_type_emission_rate'
        constraints = [
            models.UniqueConstraint(fields=["nerc", "year"], name="nerc_fuel_type_emission_rate_unique_nerc_year")
        ]


class NercFuelTypeGeneration(models.Model): 
    id = models.AutoField(primary_key=True)
    nerc = models.ForeignKey(
                NercRegion,
                to_field='nerc',
                on_delete=models.CASCADE,  # Deletes NercFuelTypeGeneration records if the related Plant is deleted
                db_column='nerc'          
            ) 
    nrgenacl = models.FloatField(blank=True, null=True)
    nrgenaol = models.FloatField(blank=True, null=True)
    nrgenaso = models.FloatField(blank=True, null=True)
    nrgenagt = models.FloatField(blank=True, null=True)
    nrgenaof = models.FloatField(blank=True, null=True)
    nrgenaop = models.FloatField(blank=True, null=True)
    nrgenatn = models.FloatField(blank=True, null=True)
    nrgenatr = models.FloatField(blank=True, null=True)
    nrgenato = models.FloatField(blank=True, null=True)
    nrgenath = models.FloatField(blank=True, null=True)
    nrgenacy = models.FloatField(blank=True, null=True)
    nrgenacn = models.FloatField(blank=True, null=True)
    nrgenaco = models.FloatField(blank=True, null=True)
    nrgenags = models.FloatField(blank=True, null=True)
    nrgenanc = models.FloatField(blank=True, null=True)
    nrgenahy = models.FloatField(blank=True, null=True)
    nrgenabm = models.FloatField(blank=True, null=True)
    nrgenawi = models.FloatField(blank=True, null=True)
    year     = models.IntegerField(null=True, blank=True)  

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'nerc_fuel_type_generation'
        constraints = [
            models.UniqueConstraint(fields=["nerc", "year"], name="nerc_fuel_type_generation_unique_nerc_year")
        ]


class NercNonBaseloadValues(models.Model): 
    id = models.AutoField(primary_key=True)
    nerc = models.ForeignKey(
                NercRegion,
                to_field='nerc',
                on_delete=models.CASCADE,  # Deletes NercNonBaseloadValues records if the related Plant is deleted
                db_column='nerc'          
            ) 
    nrnbnox  = models.FloatField(null=True, blank=True) 
    nrnbnxo  = models.FloatField(null=True, blank=True) 
    nrnbso2  = models.FloatField(null=True, blank=True) 
    nrnbco2  = models.FloatField(null=True, blank=True) 
    nrnbch4  = models.FloatField(null=True, blank=True) 
    nrnbn2o  = models.FloatField(null=True, blank=True) 
    nrnbc2e  = models.FloatField(null=True, blank=True) 
    nrnbhg   = models.CharField(max_length=2, null=True, blank=True) 
    nrnbgncl = models.FloatField(null=True, blank=True) 
    nrnbgnol = models.FloatField(null=True, blank=True) 
    nrnbgngs = models.FloatField(null=True, blank=True) 
    nrnbgnnc = models.FloatField(null=True, blank=True) 
    nrnbgnhy = models.FloatField(null=True, blank=True) 
    nrnbgnbm = models.FloatField(null=True, blank=True) 
    nrnbgnwi = models.FloatField(null=True, blank=True) 
    nrnbgnso = models.FloatField(null=True, blank=True) 
    nrnbgngt = models.FloatField(null=True, blank=True) 
    nrnbgnof = models.FloatField(null=True, blank=True) 
    nrnbgnop = models.FloatField(null=True, blank=True) 
    nrnbclpr = models.FloatField(null=True, blank=True) 
    nrnbolpr = models.FloatField(null=True, blank=True) 
    nrnbgspr = models.FloatField(null=True, blank=True) 
    nrnbncpr = models.FloatField(null=True, blank=True) 
    nrnbhypr = models.FloatField(null=True, blank=True) 
    nrnbbmpr = models.FloatField(null=True, blank=True) 
    nrnbwipr = models.FloatField(null=True, blank=True) 
    nrnbsopr = models.FloatField(null=True, blank=True) 
    nrnbgtpr = models.FloatField(null=True, blank=True) 
    nrnbofpr = models.FloatField(null=True, blank=True) 
    nrnboppr = models.FloatField(null=True, blank=True) 
    year     = models.IntegerField(null=True, blank=True)  

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'nerc_nonbaseload_values'
        constraints = [
            models.UniqueConstraint(fields=["nerc", "year"], name="nerc_nonbaseload_values_unique_nerc_year")
        ]


class NercResourceMix(models.Model): 
    id = models.AutoField(primary_key=True)
    nerc = models.ForeignKey(
                NercRegion,
                to_field='nerc',
                on_delete=models.CASCADE,  # Deletes NercResourceMix records if the related Plant is deleted
                db_column='nerc'          
            )  
    nrclpr = models.FloatField(blank=True, null=True)
    nrolpr = models.FloatField(blank=True, null=True)
    nrgspr = models.FloatField(blank=True, null=True)
    nrncpr = models.FloatField(blank=True, null=True)
    nrhypr = models.FloatField(blank=True, null=True)
    nrbmpr = models.FloatField(blank=True, null=True)
    nrwipr = models.FloatField(blank=True, null=True)
    nrsopr = models.FloatField(blank=True, null=True)
    nrgtpr = models.FloatField(blank=True, null=True)
    nrofpr = models.FloatField(blank=True, null=True)
    nroppr = models.FloatField(blank=True, null=True)
    nrtnpr = models.FloatField(blank=True, null=True)
    nrtrpr = models.FloatField(blank=True, null=True)
    nrtopr = models.FloatField(blank=True, null=True)
    nrthpr = models.FloatField(blank=True, null=True)
    nrcypr = models.FloatField(blank=True, null=True)
    nrcnpr = models.FloatField(blank=True, null=True)
    nrcopr = models.FloatField(blank=True, null=True)
    year   = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'nerc_resource_mix'
        constraints = [
            models.UniqueConstraint(fields=["nerc", "year"], name="nerc_resource_mix_unique_nerc_year")
        ]


class PlantDistributionSys(models.Model):
    oprcode = models.IntegerField(null=True, blank=True)
    oprname = models.CharField(max_length=255, null=False, blank=False)
    orispl = models.ForeignKey(
                Plant,
                on_delete=models.CASCADE,  # Deletes PlantAdjustedValue records if the related Plant is deleted
                db_column='orispl',        
                to_field='orispl',
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'plant_distribution_sys'
       
 
class PlantAdjustedValues(models.Model): 
    id = models.AutoField(primary_key=True) 
    orispl = models.ForeignKey(
                Plant,
                on_delete=models.CASCADE,  # Deletes PlantAdjustedValue records if the related Plant is deleted
                db_column='orispl',        
                to_field='orispl',
            )
    plhtian  = models.FloatField(null=True, blank=True)
    plhtioz  = models.FloatField(null=True, blank=True)
    plhtiant = models.FloatField(null=True, blank=True)
    plhtiozt = models.FloatField(null=True, blank=True)
    plngenan = models.FloatField(null=True, blank=True)
    plngenoz = models.FloatField(null=True, blank=True)
    plngennb = models.FloatField(null=True, blank=True)
    plnoxan  = models.FloatField(null=True, blank=True)
    plnoxoz  =  models.FloatField(null=True, blank=True)
    plso2an  = models.FloatField(null=True, blank=True)
    plco2an  = models.FloatField(null=True, blank=True)
    plch4an  = models.FloatField(null=True, blank=True)
    pln2oan  = models.FloatField(null=True, blank=True)
    plco2eqa = models.FloatField(null=True, blank=True)
    plhgan   = models.CharField(max_length=2, null=True, blank=True)
    capfac = models.FloatField(null=True, blank=True)
    year     = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'plant_adjusted_values'
        constraints = [
            models.UniqueConstraint(fields=["orispl", "year"], name="plant_adjusted_values_unique_orispl_year")
        ]


class PlantEmissionRate (models.Model):
    id = models.AutoField(primary_key=True) 
    orispl = models.ForeignKey(
                Plant,
                on_delete=models.CASCADE,  # Deletes PlantEmissionRate records if the related Plant is deleted
                db_column='orispl',
                to_field='orispl',      
            )
    plnoxrta = models.FloatField(blank=True, null=True)
    plnoxrto = models.FloatField(blank=True, null=True) 
    plso2rta = models.FloatField(blank=True, null=True)
    plco2rta = models.FloatField(blank=True, null=True)
    plch4rta = models.FloatField(blank=True, null=True)
    pln2orta = models.FloatField(blank=True, null=True)
    plc2erta = models.FloatField(blank=True, null=True)
    plhgrta  = models.CharField(max_length=2, blank=True, null=True) 
    plnoxra  = models.FloatField(blank=True, null=True)
    plnoxro  = models.FloatField(blank=True, null=True)
    plso2ra  = models.FloatField(blank=True, null=True)
    plco2ra  = models.FloatField(blank=True, null=True)
    plch4ra  = models.FloatField(blank=True, null=True)
    pln2ora  = models.FloatField(blank=True, null=True)
    plc2era  = models.FloatField(blank=True, null=True)
    plhgra   = models.CharField(max_length=2, blank=True, null=True) 
    plnoxcrt = models.FloatField(blank=True, null=True)
    plnoxcro = models.FloatField(blank=True, null=True)
    plso2crt = models.FloatField(blank=True, null=True)
    plco2crt = models.FloatField(blank=True, null=True)
    plch4crt = models.FloatField(blank=True, null=True)
    pln2ocrt = models.FloatField(blank=True, null=True)
    plc2ecrt = models.FloatField(blank=True, null=True)
    plhgcrt  = models.CharField(max_length=2, blank=True, null=True) 
    year     = models.IntegerField(null=True, blank=True)  # Year
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'plant_emission_rate'
        constraints = [
            models.UniqueConstraint(fields=["orispl", "year"], name="plant_emission_rate_unique_orispl_year")
        ]


class PlantFuelTypeGeneration (models.Model): 
    id = models.AutoField(primary_key=True) 
    orispl = models.ForeignKey(
                Plant,
                on_delete=models.CASCADE,  # Deletes PlantFuelTypeGeneration records if the related Plant is deleted
                db_column='orispl',   
                to_field='orispl',      
            )
    plgenacl = models.FloatField(null=True, blank=True)
    plgenaol = models.FloatField(null=True, blank=True)
    plgenags = models.FloatField(null=True, blank=True)
    plgenanc = models.FloatField(null=True, blank=True)
    plgenahy = models.FloatField(null=True, blank=True)
    plgenabm = models.FloatField(null=True, blank=True)
    plgenawi = models.FloatField(null=True, blank=True)
    plgenaso = models.FloatField(null=True, blank=True)
    plgenagt = models.FloatField(null=True, blank=True)
    plgenaof = models.FloatField(null=True, blank=True)
    plgenaop = models.FloatField(null=True, blank=True)
    plgenacy = models.FloatField(null=True, blank=True) 
    plgenacn = models.FloatField(null=True, blank=True) 
    plgenaco = models.FloatField(null=True, blank=True)
    plgenatn = models.FloatField(null=True, blank=True) 
    plgenatr = models.FloatField(null=True, blank=True) 
    plgenato = models.FloatField(null=True, blank=True)
    plgenath = models.FloatField(null=True, blank=True) 
    year     = models.IntegerField(null=True, blank=True)  # Year
 
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'plant_fuel_type_generation'
        constraints = [
            models.UniqueConstraint(fields=["orispl", "year"], name="plant_fuel_type_gen_unique_orispl_year")
        ]


class PlantResourceMix(models.Model):
    id = models.AutoField(primary_key=True) 
    orispl = models.ForeignKey(
                Plant,
                on_delete=models.CASCADE,  # Deletes PlantResourceMix records if the related Plant is deleted
                db_column='orispl',  
                to_field='orispl',        
            )
    plclpr = models.FloatField(null=True, blank=True)
    plolpr = models.FloatField(null=True, blank=True)
    plgspr = models.FloatField(null=True, blank=True)
    plncpr = models.FloatField(null=True, blank=True)
    plhypr = models.FloatField(null=True, blank=True)
    plbmpr = models.FloatField(null=True, blank=True)
    plwipr = models.FloatField(null=True, blank=True)
    plsopr = models.FloatField(null=True, blank=True)
    plgtpr = models.FloatField(null=True, blank=True)
    plofpr = models.FloatField(null=True, blank=True)
    ploppr = models.FloatField(null=True, blank=True)
    pltnpr = models.FloatField(null=True, blank=True)
    pltrpr = models.FloatField(null=True, blank=True)
    pltopr = models.FloatField(null=True, blank=True)
    plthpr = models.FloatField(null=True, blank=True)
    plcypr = models.FloatField(null=True, blank=True)
    plcnpr = models.FloatField(null=True, blank=True)
    plcopr = models.FloatField(null=True, blank=True)
    year   = models.IntegerField(null=True, blank=True)  # Year
 
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'plant_resource_mix'
        constraints = [
            models.UniqueConstraint(fields=["orispl", "year"], name="plant_resource_mix_unique_orispl_year")
        ]


class PlantUnadjustedValues(models.Model): 
    id = models.AutoField(primary_key=True) 
    orispl = models.ForeignKey(
                Plant,
                on_delete=models.CASCADE,  # Deletes PlantUnadjustedValues records if the related Plant is deleted
                db_column='orispl',
                to_field='orispl',          
            )
    unnox     = models.FloatField(null=True, blank=True)
    unnoxoz   = models.FloatField(null=True, blank=True)
    unso2     = models.FloatField(null=True, blank=True)
    unco2     = models.FloatField(null=True, blank=True)
    unch4     = models.FloatField(null=True, blank=True)
    unn2o     = models.FloatField(null=True, blank=True)
    unco2e    = models.FloatField(null=True, blank=True)
    unhg      = models.CharField(max_length=2, null=True, blank=True)
    unhti     = models.FloatField(null=True, blank=True)
    unhtioz   = models.FloatField(null=True, blank=True)
    unhtit    = models.FloatField(null=True, blank=True)
    unhtiozt  = models.FloatField(null=True, blank=True)
    unnoxsrc  = models.CharField(max_length=15, null=True, blank=True)
    unnozsrc  = models.CharField(max_length=15, null=True, blank=True)
    unso2src  = models.CharField(max_length=15, null=True, blank=True)
    unco2src  = models.CharField(max_length=15, null=True, blank=True)
    unch4src  = models.CharField(max_length=15, null=True, blank=True)
    unn2osrc  = models.CharField(max_length=15, null=True, blank=True)
    unc2esrc  = models.CharField(max_length=15, null=True, blank=True)
    unhgsrc   = models.CharField(max_length=2, null=True, blank=True)
    unhtisrc  = models.CharField(max_length=15, null=True, blank=True)
    unhozsrc  = models.CharField(max_length=15, null=True, blank=True)
    bionox    = models.FloatField(null=True, blank=True)
    bionoxoz  = models.FloatField(null=True, blank=True)
    bioso2    = models.FloatField(null=True, blank=True)
    bioco2    = models.FloatField(null=True, blank=True)
    bioch4    = models.FloatField(null=True, blank=True)
    bion2o    = models.FloatField(null=True, blank=True)
    bioco2e   = models.FloatField(null=True, blank=True)
    chpchti   = models.FloatField(null=True, blank=True)
    chpchtioz = models.FloatField(null=True, blank=True)
    chpnox    = models.FloatField(null=True, blank=True)
    chpnoxoz  = models.FloatField(null=True, blank=True)
    chpso2    = models.FloatField(null=True, blank=True)
    chpco2    = models.FloatField(null=True, blank=True)
    chpch4    = models.FloatField(null=True, blank=True)
    chpn2o    = models.FloatField(null=True, blank=True)
    chpco2e   = models.FloatField(null=True, blank=True)
    year      = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'plant_unadjusted_values'
        constraints = [
            models.UniqueConstraint(fields=["orispl", "year"], name="plant_unadjusted_values_unique_orispl_year")
        ]


class Sector(models.Model):
    sector_id = models.AutoField(primary_key=True)  
    sector = models.CharField(max_length=500, null=False, blank=False)
   
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sector'
 
class State(models.Model):
    fipsst = models.CharField(max_length=2, null=False, blank=False, unique=True)
    pstatabb = models.CharField(max_length=2, null=False, blank=False)
    stnamepcap = models.FloatField(null=True, blank=True)
   
    class Meta:
        db_table = 'state'
 
class StateAdjustedValues(models.Model): 
    id     = models.AutoField(primary_key=True)
    fipsst = models.ForeignKey(
                State,
                to_field='fipsst',
                on_delete=models.CASCADE,  # Deletes StateAdjustedValues records if the related Plant is deleted
                db_column='fipsst'          
            )  
    stnamepcap = models.FloatField(null=True, blank=True)
    sthtian    = models.FloatField(null=True, blank=True)
    sthtioz    = models.FloatField(null=True, blank=True)
    sthtiant   = models.FloatField(null=True, blank=True)
    sthtiozt   = models.FloatField(null=True, blank=True)
    stngenan   = models.FloatField(null=True, blank=True)
    stngenoz   = models.FloatField(null=True, blank=True)
    stngennb   = models.FloatField(null=True, blank=True)
    stnoxan    = models.FloatField(null=True, blank=True)
    stnoxoz    = models.FloatField(null=True, blank=True)
    stso2an    = models.FloatField(null=True, blank=True)
    stco2an    = models.FloatField(null=True, blank=True)
    stch4an    = models.FloatField(null=True, blank=True)
    stn2oan    = models.FloatField(null=True, blank=True)
    stco2eqa   = models.FloatField(null=True, blank=True)
    sthgan     = models.CharField(max_length=2, null=True, blank=True) 
    year       = models.IntegerField(null=True, blank=True)  
 
    class Meta:
        db_table = 'state_adjusted_values'
        constraints = [
            models.UniqueConstraint(fields=["fipsst", "year"], name="state_adjusted_values_unique_fipsst_year")
        ]


class Subregion(models.Model): 
    subrgn = models.CharField(primary_key=True, max_length=4, null=False, blank=False, unique=True)
    srname = models.CharField(max_length=255, null=False, blank=False)
    srnamepcap = models.FloatField(null=True, blank=True)
     
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subregion'


class StateEmissionRate(models.Model):
    id = models.AutoField(primary_key=True)
    fipsst = models.ForeignKey(
                State,
                to_field='fipsst',
                on_delete=models.CASCADE,  # Deletes StateEmissionRate records if the related Plant is deleted
                db_column='fipsst'          
            )  
    stnoxrta = models.FloatField(null=True, blank=True)
    stnoxrto = models.FloatField(null=True, blank=True)
    stso2rta = models.FloatField(null=True, blank=True)
    stco2rta = models.FloatField(null=True, blank=True)
    stch4rta = models.FloatField(null=True, blank=True)
    stn2orta = models.FloatField(null=True, blank=True)
    stc2erta = models.FloatField(null=True, blank=True)
    sthgrta  = models.CharField(max_length=2, null=True, blank=True)
    stnoxra  = models.FloatField(null=True, blank=True)
    stnoxro  = models.FloatField(null=True, blank=True)
    stso2ra  = models.FloatField(null=True, blank=True)
    stco2ra  = models.FloatField(null=True, blank=True)
    stch4ra  = models.FloatField(null=True, blank=True)
    stn2ora  = models.FloatField(null=True, blank=True)
    stc2era  = models.FloatField(null=True, blank=True)
    sthgra   = models.CharField(max_length=2, null=True, blank=True)
    stnoxcrt = models.FloatField(null=True, blank=True)
    stnoxcro = models.FloatField(null=True, blank=True)
    stso2crt = models.FloatField(null=True, blank=True)
    stco2crt = models.FloatField(null=True, blank=True)
    stch4crt = models.FloatField(null=True, blank=True)
    stn2ocrt = models.FloatField(null=True, blank=True)
    stc2ecrt = models.FloatField(null=True, blank=True)
    sthgcrt  = models.CharField(max_length=2, null=True, blank=True) 
    year     = models.IntegerField(null=True, blank=True)  

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'state_emission_rate'
        constraints = [
            models.UniqueConstraint(fields=["fipsst", "year"], name="state_emission_rate_unique_fipsst_year")
        ]


class StateFuelTypeEmissionRate(models.Model): 
    id = models.AutoField(primary_key=True)
    fipsst = models.ForeignKey(
                State,
                to_field='fipsst',
                on_delete=models.CASCADE,  # Deletes StateFuelTypeEmissionRate records if the related Plant is deleted
                db_column='fipsst'          
            )  
    stcnoxrt  = models.FloatField(blank=True, null=True)
    stonoxrt  = models.FloatField(blank=True, null=True)
    stgnoxrt  = models.FloatField(blank=True, null=True)
    stfsnxrt  = models.FloatField(blank=True, null=True)
    stcnxort  = models.FloatField(blank=True, null=True)
    stonxort  = models.FloatField(blank=True, null=True)
    stgnxort  = models.FloatField(blank=True, null=True)
    stfsnort  = models.FloatField(blank=True, null=True)
    stcso2rt  = models.FloatField(blank=True, null=True)
    stoso2rt  = models.FloatField(blank=True, null=True)
    stgso2rt  = models.FloatField(blank=True, null=True)
    stfss2rt  = models.FloatField(blank=True, null=True)
    stcco2rt  = models.FloatField(blank=True, null=True)
    stoco2rt  = models.FloatField(blank=True, null=True)
    stgco2rt  = models.FloatField(blank=True, null=True)
    stfsc2rt  = models.FloatField(blank=True, null=True)
    stcch4rt  = models.FloatField(blank=True, null=True)
    stoch4rt  = models.FloatField(blank=True, null=True)
    stgch4rt  = models.FloatField(blank=True, null=True)
    stfch4rt  = models.FloatField(blank=True, null=True)
    stcn2ort  = models.FloatField(blank=True, null=True)
    ston2ort  = models.FloatField(blank=True, null=True)
    stgn2ort  = models.FloatField(blank=True, null=True)
    stfn2ort  = models.FloatField(blank=True, null=True)
    stcc2ert  = models.FloatField(blank=True, null=True)
    stoc2ert  = models.FloatField(blank=True, null=True)
    stgc2ert  = models.FloatField(blank=True, null=True)
    stfsc2ert = models.FloatField(blank=True, null=True)
    stchgrt   = models.CharField(max_length=2, blank=True, null=True)
    stfshgrt  = models.CharField(max_length=2, blank=True, null=True)
    stcnoxr   = models.FloatField(blank=True, null=True)
    stonoxr   = models.FloatField(blank=True, null=True)
    stgnoxr   = models.FloatField(blank=True, null=True)
    stfsnxr   = models.FloatField(blank=True, null=True)
    stcnxor   = models.FloatField(blank=True, null=True)
    stonxor   = models.FloatField(blank=True, null=True)
    stgnxor   = models.FloatField(blank=True, null=True)
    stfsnor   = models.FloatField(blank=True, null=True)
    stcso2r   = models.FloatField(blank=True, null=True)
    stoso2r   = models.FloatField(blank=True, null=True)
    stgso2r   = models.FloatField(blank=True, null=True)
    stfss2r   = models.FloatField(blank=True, null=True)
    stcco2r   = models.FloatField(blank=True, null=True)
    stoco2r   = models.FloatField(blank=True, null=True)
    stgco2r   = models.FloatField(blank=True, null=True)
    stfsc2r   = models.FloatField(blank=True, null=True)
    stcch4r   = models.FloatField(blank=True, null=True)
    stoch4r   = models.FloatField(blank=True, null=True)
    stgch4r   = models.FloatField(blank=True, null=True)
    stfch4r   = models.FloatField(blank=True, null=True)
    stcn2or   = models.FloatField(blank=True, null=True)
    ston2or   = models.FloatField(blank=True, null=True)
    stgn2or   = models.FloatField(blank=True, null=True)
    stfn2or   = models.FloatField(blank=True, null=True)
    stcc2er   = models.FloatField(blank=True, null=True)
    stoc2er   = models.FloatField(blank=True, null=True)
    stgc2er   = models.FloatField(blank=True, null=True)
    stfsc2er  = models.FloatField(blank=True, null=True)
    stchgr    = models.CharField(max_length=2, blank=True, null=True)
    stfshgr   = models.CharField(max_length=2, blank=True, null=True)
    year      = models.IntegerField(null=True, blank=True)  

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'state_fuel_type_emission_rate'
        constraints = [
            models.UniqueConstraint(fields=["fipsst", "year"], name="state_fuel_type_emission_rate_unique_fipsst_year")
        ]


class StateFuelTypeGeneration(models.Model): 
    id = models.AutoField(primary_key=True)
    fipsst = models.ForeignKey(
                State,
                to_field='fipsst',
                on_delete=models.CASCADE,  # Deletes StateFuelTypeEmissionRate records if the related Plant is deleted
                db_column='fipsst'          
            )  
    stgenacl = models.FloatField(blank=True, null=True)
    stgenaol = models.FloatField(blank=True, null=True)
    stgenaso = models.FloatField(blank=True, null=True)
    stgenagt = models.FloatField(blank=True, null=True)
    stgenaof = models.FloatField(blank=True, null=True)
    stgenaop = models.FloatField(blank=True, null=True)
    stgenatn = models.FloatField(blank=True, null=True)
    stgenatr = models.FloatField(blank=True, null=True)
    stgenato = models.FloatField(blank=True, null=True)
    stgenath = models.FloatField(blank=True, null=True)
    stgenacy = models.FloatField(blank=True, null=True)
    stgenacn = models.FloatField(blank=True, null=True)
    stgenaco = models.FloatField(blank=True, null=True)
    stgenags = models.FloatField(blank=True, null=True)
    stgenanc = models.FloatField(blank=True, null=True)
    stgenahy = models.FloatField(blank=True, null=True)
    stgenabm = models.FloatField(blank=True, null=True)
    stgenawi = models.FloatField(blank=True, null=True)
    year     = models.IntegerField(null=True, blank=True)  

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'state_fuel_type_generation'
        constraints = [
            models.UniqueConstraint(fields=["fipsst", "year"], name="state_fuel_type_generation_unique_fipsst_year")
        ]


class StateNonBaseloadValues(models.Model): 
    id = models.AutoField(primary_key=True)
    fipsst = models.ForeignKey(
                State,
                to_field='fipsst',
                on_delete=models.CASCADE,  # Deletes StateFuelTypeEmissionRate records if the related Plant is deleted
                db_column='fipsst'          
            )   
    stnbnox  = models.FloatField(null=True, blank=True) 
    stnbnxo  = models.FloatField(null=True, blank=True) 
    stnbso2  = models.FloatField(null=True, blank=True) 
    stnbco2  = models.FloatField(null=True, blank=True) 
    stnbch4  = models.FloatField(null=True, blank=True) 
    stnbn2o  = models.FloatField(null=True, blank=True) 
    stnbc2e  = models.FloatField(null=True, blank=True) 
    stnbhg   = models.CharField(max_length=2, null=True, blank=True) 
    stnbgncl = models.FloatField(null=True, blank=True) 
    stnbgnol = models.FloatField(null=True, blank=True) 
    stnbgngs = models.FloatField(null=True, blank=True) 
    stnbgnnc = models.FloatField(null=True, blank=True) 
    stnbgnhy = models.FloatField(null=True, blank=True) 
    stnbgnbm = models.FloatField(null=True, blank=True) 
    stnbgnwi = models.FloatField(null=True, blank=True) 
    stnbgnso = models.FloatField(null=True, blank=True) 
    stnbgngt = models.FloatField(null=True, blank=True) 
    stnbgnof = models.FloatField(null=True, blank=True) 
    stnbgnop = models.FloatField(null=True, blank=True) 
    stnbclpr = models.FloatField(null=True, blank=True) 
    stnbolpr = models.FloatField(null=True, blank=True) 
    stnbgspr = models.FloatField(null=True, blank=True) 
    stnbncpr = models.FloatField(null=True, blank=True) 
    stnbhypr = models.FloatField(null=True, blank=True) 
    stnbbmpr = models.FloatField(null=True, blank=True) 
    stnbwipr = models.FloatField(null=True, blank=True) 
    stnbsopr = models.FloatField(null=True, blank=True) 
    stnbgtpr = models.FloatField(null=True, blank=True) 
    stnbofpr = models.FloatField(null=True, blank=True) 
    stnboppr = models.FloatField(null=True, blank=True) 
    year     = models.IntegerField(null=True, blank=True)  

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'state_nonbaseload_values'
        constraints = [
            models.UniqueConstraint(fields=["fipsst", "year"], name="state_nonbaseload_values_unique_fipsst_year")
        ]

class StateResourceMix(models.Model): 
    id = models.AutoField(primary_key=True)
    fipsst = models.ForeignKey(
                State,
                to_field='fipsst',
                on_delete=models.CASCADE,  # Deletes StateFuelTypeEmissionRate records if the related Plant is deleted
                db_column='fipsst'          
            )   
    stclpr = models.FloatField(blank=True, null=True)
    stolpr = models.FloatField(blank=True, null=True)
    stgspr = models.FloatField(blank=True, null=True)
    stncpr = models.FloatField(blank=True, null=True)
    sthypr = models.FloatField(blank=True, null=True)
    stbmpr = models.FloatField(blank=True, null=True)
    stwipr = models.FloatField(blank=True, null=True)
    stsopr = models.FloatField(blank=True, null=True)
    stgtpr = models.FloatField(blank=True, null=True)
    stofpr = models.FloatField(blank=True, null=True)
    stoppr = models.FloatField(blank=True, null=True)
    sttnpr = models.FloatField(blank=True, null=True)
    sttrpr = models.FloatField(blank=True, null=True)
    sttopr = models.FloatField(blank=True, null=True)
    stthpr = models.FloatField(blank=True, null=True)
    stcypr = models.FloatField(blank=True, null=True)
    stcnpr = models.FloatField(blank=True, null=True)
    stcopr = models.FloatField(blank=True, null=True)
    year   = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'state_resource_mix'
        constraints = [
            models.UniqueConstraint(fields=["fipsst", "year"], name="state_resource_mix_unique_fipsst_year")
        ]

class SubrgnAdjustedValues(models.Model): 
    id = models.AutoField(primary_key=True)
    subrgn = models.ForeignKey(
                Subregion,
                on_delete=models.CASCADE,  # Deletes SubrgnAdjustedValues records if the related Plant is deleted
                db_column='subrgn'          
            ) 
    srhtian   = models.FloatField(null=True, blank=True)
    srhtioz   = models.FloatField(null=True, blank=True)
    srhtiant  = models.FloatField(null=True, blank=True)
    srhtiozt  = models.FloatField(null=True, blank=True)
    srngenan  = models.FloatField(null=True, blank=True)
    srngenoz  = models.FloatField(null=True, blank=True)
    srngennb  = models.FloatField(null=True, blank=True)
    srnoxan   = models.FloatField(null=True, blank=True)
    srnoxoz   = models.FloatField(null=True, blank=True)
    srso2an   = models.FloatField(null=True, blank=True)
    srco2an   = models.FloatField(null=True, blank=True)
    srch4an   = models.FloatField(null=True, blank=True)
    srn2oan   = models.FloatField(null=True, blank=True)
    srco2eqa  = models.FloatField(null=True, blank=True)
    srhgan    = models.CharField(max_length=2, null=True, blank=True) 
    year      = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subrgn_adjusted_values'
        constraints = [
            models.UniqueConstraint(fields=["subrgn", "year"], name="subregion_adjusted_values_unique_subrgn_year")
        ]

class SubrgnEmissionRate(models.Model): 
    id = models.AutoField(primary_key=True)
    subrgn = models.ForeignKey(
                Subregion,
                on_delete=models.CASCADE,  # Deletes SubrgnEmissionRate records if the related Plant is deleted
                db_column='subrgn'          
            ) 
    srnoxrta = models.FloatField(blank=True, null=True)
    srnoxrto = models.FloatField(blank=True, null=True)
    srso2rta = models.FloatField(blank=True, null=True)
    srco2rta = models.FloatField(blank=True, null=True)
    srch4rta = models.FloatField(blank=True, null=True)
    srn2orta = models.FloatField(blank=True, null=True)
    src2erta = models.FloatField(blank=True, null=True)
    srhgrta  = models.CharField(max_length=2, blank=True, null=True)
    srnoxra  = models.FloatField(blank=True, null=True)
    srnoxro  = models.FloatField(blank=True, null=True)
    srso2ra  = models.FloatField(blank=True, null=True)
    srco2ra  = models.FloatField(blank=True, null=True)
    srch4ra  = models.FloatField(blank=True, null=True)
    srn2ora  = models.FloatField(blank=True, null=True)
    src2era  = models.FloatField(blank=True, null=True)
    srhgra   = models.CharField(max_length=2, blank=True, null=True)
    srnoxcrt = models.FloatField(blank=True, null=True)
    srnoxcro = models.FloatField(blank=True, null=True)
    srso2crt = models.FloatField(blank=True, null=True)
    srco2crt = models.FloatField(blank=True, null=True)
    srch4crt = models.FloatField(blank=True, null=True)
    srn2ocrt = models.FloatField(blank=True, null=True)
    src2ecrt = models.FloatField(blank=True, null=True)
    srhgcrt  = models.CharField(max_length=2, blank=True, null=True)
    year     = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subrgn_emission_rate'
        constraints = [
            models.UniqueConstraint(fields=["subrgn", "year"], name="subregion_emission_rate_unique_subrgn_year")
        ]
  
class SubrgnFuelTypeEmissionRate(models.Model):  
    id = models.AutoField(primary_key=True)
    subrgn = models.ForeignKey(
                Subregion,
                on_delete=models.CASCADE,  # Deletes SubrgnFuelTypeEmissionRate records if the related Plant is deleted
                db_column='subrgn'          
            ) 
    srcnoxrt  = models.FloatField(blank=True, null=True)
    sronoxrt  = models.FloatField(blank=True, null=True)
    srgnoxrt  = models.FloatField(blank=True, null=True)
    srfsnxrt  = models.FloatField(blank=True, null=True)
    srcnxort  = models.FloatField(blank=True, null=True)
    sronxort  = models.FloatField(blank=True, null=True)
    srgnxort  = models.FloatField(blank=True, null=True)
    srfsnort  = models.FloatField(blank=True, null=True)
    srcso2rt  = models.FloatField(blank=True, null=True)
    sroso2rt  = models.FloatField(blank=True, null=True)
    srgso2rt  = models.FloatField(blank=True, null=True)
    srfss2rt  = models.FloatField(blank=True, null=True)
    srcco2rt  = models.FloatField(blank=True, null=True)
    sroco2rt  = models.FloatField(blank=True, null=True)
    srgco2rt  = models.FloatField(blank=True, null=True)
    srfsc2rt  = models.FloatField(blank=True, null=True)
    srcch4rt  = models.FloatField(blank=True, null=True)
    sroch4rt  = models.FloatField(blank=True, null=True)
    srgch4rt  = models.FloatField(blank=True, null=True)
    srfch4rt  = models.FloatField(blank=True, null=True)
    srcn2ort  = models.FloatField(blank=True, null=True)
    sron2ort  = models.FloatField(blank=True, null=True)
    srgn2ort  = models.FloatField(blank=True, null=True)
    srfn2ort  = models.FloatField(blank=True, null=True)
    srcc2ert  = models.FloatField(blank=True, null=True)
    sroc2ert  = models.FloatField(blank=True, null=True)
    srgc2ert  = models.FloatField(blank=True, null=True)
    srfsc2ert = models.FloatField(blank=True, null=True)
    srchgrt   = models.CharField(max_length=2, blank=True, null=True)
    srfshgrt  = models.CharField(max_length=2, blank=True, null=True)
    srcnoxr   = models.FloatField(blank=True, null=True)
    sronoxr   = models.FloatField(blank=True, null=True)
    srgnoxr   = models.FloatField(blank=True, null=True)
    srfsnxr   = models.FloatField(blank=True, null=True)
    srcnxor   = models.FloatField(blank=True, null=True)
    sronxor   = models.FloatField(blank=True, null=True)
    srgnxor   = models.FloatField(blank=True, null=True)
    srfsnor   = models.FloatField(blank=True, null=True)
    srcso2r   = models.FloatField(blank=True, null=True)
    sroso2r   = models.FloatField(blank=True, null=True)
    srgso2r   = models.FloatField(blank=True, null=True)
    srfss2r   = models.FloatField(blank=True, null=True)
    srcco2r   = models.FloatField(blank=True, null=True)
    sroco2r   = models.FloatField(blank=True, null=True)
    srgco2r   = models.FloatField(blank=True, null=True)
    srfsc2r   = models.FloatField(blank=True, null=True)
    srcch4r   = models.FloatField(blank=True, null=True)
    sroch4r   = models.FloatField(blank=True, null=True)
    srgch4r   = models.FloatField(blank=True, null=True)
    srfch4r   = models.FloatField(blank=True, null=True)
    srcn2or   = models.FloatField(blank=True, null=True)
    sron2or   = models.FloatField(blank=True, null=True)
    srgn2or   = models.FloatField(blank=True, null=True)
    srfn2or   = models.FloatField(blank=True, null=True)
    srcc2er   = models.FloatField(blank=True, null=True)
    sroc2er   = models.FloatField(blank=True, null=True)
    srgc2er   = models.FloatField(blank=True, null=True)
    srfsc2er  = models.FloatField(blank=True, null=True)
    srchgr    = models.CharField(max_length=2, blank=True, null=True)
    srfshgr   = models.CharField(max_length=2, blank=True, null=True)
    year      = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subrgn_fuel_type_emission_rate'
        constraints = [
            models.UniqueConstraint(fields=["subrgn", "year"], name="subregion_fuel_type_emission_rate_unique_subrgn_year")
        ]

class SubrgnFuelTypeGeneration(models.Model): 
    id = models.AutoField(primary_key=True)
    subrgn = models.ForeignKey(
                Subregion,
                on_delete=models.CASCADE,  # Deletes SubrgnFuelTypeGeneration records if the related Plant is deleted
                db_column='subrgn'          
            ) 
    srgenacl = models.FloatField(blank=True, null=True)
    srgenaol = models.FloatField(blank=True, null=True)
    srgenaso = models.FloatField(blank=True, null=True)
    srgenagt = models.FloatField(blank=True, null=True)
    srgenaof = models.FloatField(blank=True, null=True)
    srgenaop = models.FloatField(blank=True, null=True)
    srgenatn = models.FloatField(blank=True, null=True)
    srgenatr = models.FloatField(blank=True, null=True)
    srgenato = models.FloatField(blank=True, null=True)
    srgenath = models.FloatField(blank=True, null=True)
    srgenacy = models.FloatField(blank=True, null=True)
    srgenacn = models.FloatField(blank=True, null=True)
    srgenaco = models.FloatField(blank=True, null=True)
    srgenags = models.FloatField(blank=True, null=True)
    srgenanc = models.FloatField(blank=True, null=True)
    srgenahy = models.FloatField(blank=True, null=True)
    srgenabm = models.FloatField(blank=True, null=True)
    srgenawi = models.FloatField(blank=True, null=True)
    year     = models.IntegerField(null=True, blank=True)  

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subrgn_fuel_type_generation'
        constraints = [
            models.UniqueConstraint(fields=["subrgn", "year"], name="subregion_fuel_type_generation_unique_subrgn_year")
        ]


class SubrgnNonBaseloadValues(models.Model): 
    id = models.AutoField(primary_key=True)
    subrgn = models.ForeignKey(
                Subregion,
                on_delete=models.CASCADE,  # Deletes SubrgnNonBaseloadValues records if the related Plant is deleted
                db_column='subrgn'          
            ) 
    srnbnox  = models.FloatField(null=True, blank=True) 
    srnbnxo  = models.FloatField(null=True, blank=True) 
    srnbso2  = models.FloatField(null=True, blank=True) 
    srnbco2  = models.FloatField(null=True, blank=True) 
    srnbch4  = models.FloatField(null=True, blank=True) 
    srnbn2o  = models.FloatField(null=True, blank=True) 
    srnbc2e  = models.FloatField(null=True, blank=True) 
    srnbhg   = models.CharField(max_length=2, null=True, blank=True) 
    srnbgncl = models.FloatField(null=True, blank=True) 
    srnbgnol = models.FloatField(null=True, blank=True) 
    srnbgngs = models.FloatField(null=True, blank=True) 
    srnbgnnc = models.FloatField(null=True, blank=True) 
    srnbgnhy = models.FloatField(null=True, blank=True) 
    srnbgnbm = models.FloatField(null=True, blank=True) 
    srnbgnwi = models.FloatField(null=True, blank=True) 
    srnbgnso = models.FloatField(null=True, blank=True) 
    srnbgngt = models.FloatField(null=True, blank=True) 
    srnbgnof = models.FloatField(null=True, blank=True) 
    srnbgnop = models.FloatField(null=True, blank=True) 
    srnbclpr = models.FloatField(null=True, blank=True) 
    srnbolpr = models.FloatField(null=True, blank=True) 
    srnbgspr = models.FloatField(null=True, blank=True) 
    srnbncpr = models.FloatField(null=True, blank=True) 
    srnbhypr = models.FloatField(null=True, blank=True) 
    srnbbmpr = models.FloatField(null=True, blank=True) 
    srnbwipr = models.FloatField(null=True, blank=True) 
    srnbsopr = models.FloatField(null=True, blank=True) 
    srnbgtpr = models.FloatField(null=True, blank=True) 
    srnbofpr = models.FloatField(null=True, blank=True) 
    srnboppr = models.FloatField(null=True, blank=True) 
    year     = models.IntegerField(null=True, blank=True)  

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subrgn_nonbaseload_values'
        constraints = [
            models.UniqueConstraint(fields=["subrgn", "year"], name="subregion_nonbaseload_values_unique_subrgn_year")
        ]

class SubrgnResourceMix(models.Model): 
    id = models.AutoField(primary_key=True)
    subrgn = models.ForeignKey(
                Subregion,
                on_delete=models.CASCADE,  # Deletes SubrgnResourceMix records if the related Plant is deleted
                db_column='subrgn'          
            )  
    srclpr = models.FloatField(blank=True, null=True)
    srolpr = models.FloatField(blank=True, null=True)
    srgspr = models.FloatField(blank=True, null=True)
    srncpr = models.FloatField(blank=True, null=True)
    srhypr = models.FloatField(blank=True, null=True)
    srbmpr = models.FloatField(blank=True, null=True)
    srwipr = models.FloatField(blank=True, null=True)
    srsopr = models.FloatField(blank=True, null=True)
    srgtpr = models.FloatField(blank=True, null=True)
    srofpr = models.FloatField(blank=True, null=True)
    sroppr = models.FloatField(blank=True, null=True)
    srtnpr = models.FloatField(blank=True, null=True)
    srtrpr = models.FloatField(blank=True, null=True)
    srtopr = models.FloatField(blank=True, null=True)
    srthpr = models.FloatField(blank=True, null=True)
    srcypr = models.FloatField(blank=True, null=True)
    srcnpr = models.FloatField(blank=True, null=True)
    srcopr = models.FloatField(blank=True, null=True)
    year   = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subrgn_resource_mix'
        constraints = [
            models.UniqueConstraint(fields=["subrgn", "year"], name="subregion_resource_mix_unique_subrgn_year")
        ]

# Got to go back to this
class Utility(models.Model):
    utlsrvid = models.IntegerField(primary_key=True, unique=True)
    utlsrvnm = models.CharField(max_length=500, null=False, blank=False)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'utility'


# Tables for Unit
# Table for the fields that do not change year to year
class Unit(models.Model): 
    id = models.AutoField(primary_key=True)
    unitid = models.CharField(max_length=100, null=False, blank=False)
    orispl = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,  # Deletes Unit records if the related Plant is deleted
        db_column='orispl',   
        to_field='orispl'       
    ) 
    prmvr    = models.CharField(max_length=2, null=True, blank=True) 
    capdflag = models.CharField(max_length=50, null=True, blank=True)
    prgcode  = models.CharField(max_length=4000, null=True, blank=True)
    botfirty = models.CharField(max_length=255, null=True, blank=True)
    numgen   = models.IntegerField(null=True, blank=True)
    sequnt   = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.unitid} - {self.orispl} - {self.prmvr}"

    class Meta:
        db_table = 'unit'
        constraints = [
            models.UniqueConstraint(fields=["unitid", "orispl", "prmvr"], name="unit_composite_pk")
        ]

class UnitUnadjustedValues(models.Model): 
    id = models.AutoField(primary_key=True)
    unitid = models.CharField(max_length=100, null=False, blank=False)
    orispl = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,  # Deletes Unit records if the related Plant is deleted
        db_column='orispl',
        to_field='orispl'         
    ) 
    prmvr    = models.CharField(max_length=2, null=True, blank=True) 
    untopst  = models.CharField(max_length=100, null=True, blank=True) 
    fuelu1   = models.CharField(max_length=6, null=True, blank=True)
    hrsop    = models.FloatField(null=True, blank=True) 
    htian    = models.FloatField(null=True, blank=True)
    htioz    = models.FloatField(null=True, blank=True)
    noxan    = models.FloatField(null=True, blank=True)
    noxoz    = models.FloatField(null=True, blank=True)
    so2an    = models.FloatField(null=True, blank=True)
    co2an    = models.FloatField(null=True, blank=True)
    hgan     = models.FloatField(null=True, blank=True)
    htiansrc = models.CharField(max_length=200, null=True, blank=True)
    htiozsrc = models.CharField(max_length=200, null=True, blank=True)
    noxansrc = models.CharField(max_length=200, null=True, blank=True)
    noxozsrc = models.CharField(max_length=200, null=True, blank=True)
    so2src   = models.CharField(max_length=200, null=True, blank=True)
    co2src   = models.CharField(max_length=200, null=True, blank=True)
    hgsrc    = models.CharField(max_length=200, null=True, blank=True)
    so2ctldv = models.CharField(max_length=10, null=True, blank=True) 
    noxctldv = models.CharField(max_length=200, null=True, blank=True)
    hgctldv  = models.CharField(max_length=200, null=True, blank=True)
    untyronl = models.IntegerField(null=True, blank=True)
    stackht  = models.FloatField(null=True, blank=True)
    year   = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.unitid} - {self.orispl} - {self.prmvr}"

    class Meta:
        db_table = 'unit_unadjusted_values'
        constraints = [
            models.UniqueConstraint(fields=["unitid", "orispl", "prmvr", "year"], name="unitunadjustedvalues_composite_pk")
        ]

class US(models.Model):
    year = models.IntegerField()
    usnamepcap = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'us'
        constraints = [
            models.UniqueConstraint(fields=["usnamepcap", "year"], name="us_composite_pk")
        ]


class UsAdjustedValues(models.Model): 
    id = models.AutoField(primary_key=True)
    usnamepcap = models.FloatField(null=True, blank=True)
    ushtian    = models.FloatField(null=True, blank=True)
    ushtioz    = models.FloatField(null=True, blank=True)
    ushtiant   = models.FloatField(null=True, blank=True)
    ushtiozt   = models.FloatField(null=True, blank=True)
    usngenan   = models.FloatField(null=True, blank=True)
    usngenoz   = models.FloatField(null=True, blank=True)
    usngennb   = models.FloatField(null=True, blank=True)
    usnoxan    = models.FloatField(null=True, blank=True)
    usnoxoz    = models.FloatField(null=True, blank=True)
    usso2an    = models.FloatField(null=True, blank=True)
    usco2an    = models.FloatField(null=True, blank=True)
    usch4an    = models.FloatField(null=True, blank=True)
    usn2oan    = models.FloatField(null=True, blank=True)
    usco2eqa   = models.FloatField(null=True, blank=True)
    ushgan     = models.CharField(null=True, blank=True) 
    year       = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'us_adjusted_values'
        constraints = [
            models.UniqueConstraint(fields=["usnamepcap", "year"], name="usadjustedvalues_composite_pk")
        ]


class UsEmissionRate(models.Model): 
    id = models.AutoField(primary_key=True)
    usnoxrta = models.FloatField(blank=True, null=True)
    usnoxrto = models.FloatField(blank=True, null=True)
    usso2rta = models.FloatField(blank=True, null=True)
    usco2rta = models.FloatField(blank=True, null=True)
    usch4rta = models.FloatField(blank=True, null=True)
    usn2orta = models.FloatField(blank=True, null=True)
    usc2erta = models.FloatField(blank=True, null=True)
    ushgrta  = models.CharField(blank=True, null=True)
    usnoxra  = models.FloatField(blank=True, null=True)
    usnoxro  = models.FloatField(blank=True, null=True)
    usso2ra  = models.FloatField(blank=True, null=True)
    usco2ra  = models.FloatField(blank=True, null=True)
    usch4ra  = models.FloatField(blank=True, null=True)
    usn2ora  = models.FloatField(blank=True, null=True)
    usc2era  = models.FloatField(blank=True, null=True)
    ushgra   = models.CharField(blank=True, null=True)
    usnoxcrt = models.FloatField(blank=True, null=True)
    usnoxcro = models.FloatField(blank=True, null=True)
    usso2crt = models.FloatField(blank=True, null=True)
    usco2crt = models.FloatField(blank=True, null=True)
    usch4crt = models.FloatField(blank=True, null=True)
    usn2ocrt = models.FloatField(blank=True, null=True)
    usc2ecrt = models.FloatField(blank=True, null=True)
    ushgcrt  = models.CharField(blank=True, null=True)
    usnamepcap = models.FloatField(blank=True, null=True)
    year     = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'us_emission_rate'
        constraints = [
            models.UniqueConstraint(fields=["usnamepcap", "year"], name="usemissionrate_composite_pk")
        ]
  

class UsFuelTypeEmissionRate(models.Model):  
    id = models.AutoField(primary_key=True)
    uscnoxrt  = models.FloatField(blank=True, null=True)
    usonoxrt  = models.FloatField(blank=True, null=True)
    usgnoxrt  = models.FloatField(blank=True, null=True)
    usfsnxrt  = models.FloatField(blank=True, null=True)
    uscnxort  = models.FloatField(blank=True, null=True)
    usonxort  = models.FloatField(blank=True, null=True)
    usgnxort  = models.FloatField(blank=True, null=True)
    usfsnort  = models.FloatField(blank=True, null=True)
    uscso2rt  = models.FloatField(blank=True, null=True)
    usoso2rt  = models.FloatField(blank=True, null=True)
    usgso2rt  = models.FloatField(blank=True, null=True)
    usfss2rt  = models.FloatField(blank=True, null=True)
    uscco2rt  = models.FloatField(blank=True, null=True)
    usoco2rt  = models.FloatField(blank=True, null=True)
    usgco2rt  = models.FloatField(blank=True, null=True)
    usfsc2rt  = models.FloatField(blank=True, null=True)
    uscch4rt  = models.FloatField(blank=True, null=True)
    usoch4rt  = models.FloatField(blank=True, null=True)
    usgch4rt  = models.FloatField(blank=True, null=True)
    usfch4rt  = models.FloatField(blank=True, null=True)
    uscn2ort  = models.FloatField(blank=True, null=True)
    uson2ort  = models.FloatField(blank=True, null=True)
    usgn2ort  = models.FloatField(blank=True, null=True)
    usfn2ort  = models.FloatField(blank=True, null=True)
    uscc2ert  = models.FloatField(blank=True, null=True)
    usoc2ert  = models.FloatField(blank=True, null=True)
    usgc2ert  = models.FloatField(blank=True, null=True)
    usfsc2ert = models.FloatField(blank=True, null=True)
    uschgrt   = models.CharField(blank=True, null=True)
    usfshgrt  = models.CharField(blank=True, null=True)
    uscnoxr   = models.FloatField(blank=True, null=True)
    usonoxr   = models.FloatField(blank=True, null=True)
    usgnoxr   = models.FloatField(blank=True, null=True)
    usfsnxr   = models.FloatField(blank=True, null=True)
    uscnxor   = models.FloatField(blank=True, null=True)
    usonxor   = models.FloatField(blank=True, null=True)
    usgnxor   = models.FloatField(blank=True, null=True)
    usfsnor   = models.FloatField(blank=True, null=True)
    uscso2r   = models.FloatField(blank=True, null=True)
    usoso2r   = models.FloatField(blank=True, null=True)
    usgso2r   = models.FloatField(blank=True, null=True)
    usfss2r   = models.FloatField(blank=True, null=True)
    uscco2r   = models.FloatField(blank=True, null=True)
    usoco2r   = models.FloatField(blank=True, null=True)
    usgco2r   = models.FloatField(blank=True, null=True)
    usfsc2r   = models.FloatField(blank=True, null=True)
    uscch4r   = models.FloatField(blank=True, null=True)
    usoch4r   = models.FloatField(blank=True, null=True)
    usgch4r   = models.FloatField(blank=True, null=True)
    usfch4r   = models.FloatField(blank=True, null=True)
    uscn2or   = models.FloatField(blank=True, null=True)
    uson2or   = models.FloatField(blank=True, null=True)
    usgn2or   = models.FloatField(blank=True, null=True)
    usfn2or   = models.FloatField(blank=True, null=True)
    uscc2er   = models.FloatField(blank=True, null=True)
    usoc2er   = models.FloatField(blank=True, null=True)
    usgc2er   = models.FloatField(blank=True, null=True)
    usfsc2er  = models.FloatField(blank=True, null=True)
    uschgr    = models.CharField(blank=True, null=True)
    usfshgr   = models.CharField(blank=True, null=True)
    usnamepcap = models.FloatField(blank=True, null=True)
    year     = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'us_fuel_type_emission_rate'
        constraints = [
            models.UniqueConstraint(fields=["usnamepcap", "year"], name="usfueltypeemissionrate_composite_pk")
        ]


class UsFuelTypeGeneration(models.Model): 
    id = models.AutoField(primary_key=True)
    usgenacl = models.FloatField(blank=True, null=True)
    usgenaol = models.FloatField(blank=True, null=True)
    usgenaso = models.FloatField(blank=True, null=True)
    usgenagt = models.FloatField(blank=True, null=True)
    usgenaof = models.FloatField(blank=True, null=True)
    usgenaop = models.FloatField(blank=True, null=True)
    usgenatn = models.FloatField(blank=True, null=True)
    usgenatr = models.FloatField(blank=True, null=True)
    usgenato = models.FloatField(blank=True, null=True)
    usgenath = models.FloatField(blank=True, null=True)
    usgenacy = models.FloatField(blank=True, null=True)
    usgenacn = models.FloatField(blank=True, null=True)
    usgenaco = models.FloatField(blank=True, null=True)
    usgenags = models.FloatField(blank=True, null=True)
    usgenanc = models.FloatField(blank=True, null=True)
    usgenahy = models.FloatField(blank=True, null=True)
    usgenabm = models.FloatField(blank=True, null=True)
    usgenawi = models.FloatField(blank=True, null=True)
    usnamepcap = models.FloatField(blank=True, null=True)
    year     = models.IntegerField(null=True, blank=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'us_fuel_type_generation'
        constraints = [
            models.UniqueConstraint(fields=["usnamepcap", "year"], name="usfueltypegeneration_composite_pk")
        ]


class UsNonBaseloadValues(models.Model): 
    id = models.AutoField(primary_key=True)
    usnbnox  = models.FloatField(null=True, blank=True) 
    usnbnxo  = models.FloatField(null=True, blank=True) 
    usnbso2  = models.FloatField(null=True, blank=True) 
    usnbco2  = models.FloatField(null=True, blank=True) 
    usnbch4  = models.FloatField(null=True, blank=True) 
    usnbn2o  = models.FloatField(null=True, blank=True) 
    usnbc2e  = models.FloatField(null=True, blank=True) 
    usnbhg   = models.FloatField(null=True, blank=True) 
    usnbgncl = models.FloatField(null=True, blank=True) 
    usnbgnol = models.FloatField(null=True, blank=True) 
    usnbgngs = models.FloatField(null=True, blank=True) 
    usnbgnnc = models.FloatField(null=True, blank=True) 
    usnbgnhy = models.FloatField(null=True, blank=True) 
    usnbgnbm = models.FloatField(null=True, blank=True) 
    usnbgnwi = models.FloatField(null=True, blank=True) 
    usnbgnso = models.FloatField(null=True, blank=True) 
    usnbgngt = models.FloatField(null=True, blank=True) 
    usnbgnof = models.FloatField(null=True, blank=True) 
    usnbgnop = models.FloatField(null=True, blank=True) 
    usnbclpr = models.FloatField(null=True, blank=True) 
    usnbolpr = models.FloatField(null=True, blank=True) 
    usnbgspr = models.FloatField(null=True, blank=True) 
    usnbncpr = models.FloatField(null=True, blank=True) 
    usnbhypr = models.FloatField(null=True, blank=True) 
    usnbbmpr = models.FloatField(null=True, blank=True) 
    usnbwipr = models.FloatField(null=True, blank=True) 
    usnbsopr = models.FloatField(null=True, blank=True) 
    usnbgtpr = models.FloatField(null=True, blank=True) 
    usnbofpr = models.FloatField(null=True, blank=True) 
    usnboppr = models.FloatField(null=True, blank=True) 
    usnamepcap = models.FloatField(blank=True, null=True)
    year     = models.IntegerField(null=True, blank=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'us_nonbaseload_values'
        constraints = [
            models.UniqueConstraint(fields=["usnamepcap", "year"], name="usnonbaseloadvalues_composite_pk")
        ]


class UsResourceMix(models.Model): 
    id = models.AutoField(primary_key=True) 
    usclpr = models.FloatField(blank=True, null=True)
    usolpr = models.FloatField(blank=True, null=True)
    usgspr = models.FloatField(blank=True, null=True)
    usncpr = models.FloatField(blank=True, null=True)
    ushypr = models.FloatField(blank=True, null=True)
    usbmpr = models.FloatField(blank=True, null=True)
    uswipr = models.FloatField(blank=True, null=True)
    ussopr = models.FloatField(blank=True, null=True)
    usgtpr = models.FloatField(blank=True, null=True)
    usofpr = models.FloatField(blank=True, null=True)
    usoppr = models.FloatField(blank=True, null=True)
    ustnpr = models.FloatField(blank=True, null=True)
    ustrpr = models.FloatField(blank=True, null=True)
    ustopr = models.FloatField(blank=True, null=True)
    usthpr = models.FloatField(blank=True, null=True)
    uscypr = models.FloatField(blank=True, null=True)
    uscnpr = models.FloatField(blank=True, null=True)
    uscopr = models.FloatField(blank=True, null=True)
    usnamepcap = models.FloatField(blank=True, null=True)
    year     = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'us_resource_mix'
        constraints = [
            models.UniqueConstraint(fields=["usnamepcap", "year"], name="usresourcemix_composite_pk")
        ]
