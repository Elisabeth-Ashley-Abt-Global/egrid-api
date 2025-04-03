from django.db import models

class BalancingAuthority(models.Model): 
    bacode = models.CharField(max_length=20, primary_key=True, unique=True)  
    baname = models.CharField(max_length=255)   
    banamepcap = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "balancing_authority"

    def __str__(self):
        return self.name
    
class BAAnnualCombustion(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    # bacode = models.CharField(max_length=20, null=False, blank=False)  # BA Code
    bacode = models.ForeignKey(
        BalancingAuthority,
        on_delete=models.CASCADE,
        db_column='bacode'
    )
    bahtian = models.FloatField(null=True, blank=True, db_comment='BA annual heat input from combustion (MMBtu)')  # BA annual heat input (MMBtu)
    bahtioz = models.FloatField(null=True, blank=True)
    bahtiant = models.FloatField(null=True, blank=True)
    bahtiozt = models.FloatField(null=True, blank=True)
    bangenan = models.FloatField(null=True, blank=True)
    bangenoz = models.FloatField(null=True, blank=True)
    bangennb = models.FloatField(null=True, blank=True)
    banoxan = models.FloatField(null=True, blank=True)
    banoxoz = models.FloatField(null=True, blank=True)
    baso2an = models.FloatField(null=True, blank=True)
    baco2an = models.FloatField(null=True, blank=True)
    bach4an = models.FloatField(null=True, blank=True)
    ban2oan = models.FloatField(null=True, blank=True)
    baco2eqa = models.FloatField(null=True, blank=True)
    bahgan = models.CharField(null=True, blank=True)  
    # created_on = models.DateTimeField(auto_now_add=True)  # Automatically sets the field to the current timestamp only when the record is first created.
    # updated_on = models.DateTimeField(auto_now=True) # Automatically updates the field to the current timestamp every time the record is saved.
    year = models.IntegerField(null=True, blank=True)  # Year
 
    class Meta:
        db_table = "ba_annual_combustion"

    def __str__(self):
        return self.name

class Plant(models.Model):
    seqplt = models.IntegerField(null=True, blank=True) # seqplt
    orispl = models.IntegerField(null=False, blank=False, unique=True)  # Plant ID ADD A UNIQUE CONSTRAINT
    pstatabb = models.CharField(max_length=1000, null=True, blank=True)
    fipsst = models.CharField(max_length=1000, null=True, blank=True)  # State Id
    pname = models.CharField(max_length=1000, null=True, blank=True)
    oprcode = models.IntegerField(null=True, blank=True)
    utlsrvid = models.IntegerField(null=True, blank=True)
    sector = models.CharField(max_length=1000, null=True, blank=True)
    bacode = models.CharField(max_length=1000, null=True, blank=True)
    nerc = models.CharField(max_length=1000, null=True, blank=True)
    fipscnty = models.IntegerField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    numunt = models.IntegerField(null=True, blank=True)
    numgen = models.IntegerField(null=True, blank=True)
    plprmfl = models.CharField(max_length=1000, null=True, blank=True)
    plfuelct = models.CharField(max_length=1000, null=True, blank=True)
    coalflag = models.CharField(max_length=1000, null=True, blank=True)
    subrgn = models.CharField(null=True, blank=True, max_length=4) 
    isorto = models.CharField(null=True, blank=True, max_length=5)
    namepcap = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'plant'

 
class BaEmissionRate(models.Model):
    id     =  models.AutoField(primary_key=True) 
    bacode = models.ForeignKey(
        BalancingAuthority,
        on_delete=models.CASCADE,  # Deletes BAAnnualCombustion records if the related BalancingAuthority is deleted
        db_column='bacode'          # Ensures the column in the database is still named 'bacode'
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

class BaFuelTypeEmissionRate(models.Model):
    id       =  models.AutoField(primary_key=True) 
    bacode = models.ForeignKey(
        BalancingAuthority,
        on_delete=models.CASCADE,  # Deletes BAAnnualCombustion records if the related BalancingAuthority is deleted
        db_column='bacode'          # Ensures the column in the database is still named 'ba_id'
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
    bachgrt   = models.CharField(blank=True, null=True) 
    bafshgrt  = models.CharField(blank=True, null=True) 
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
    bachgr    = models.CharField(blank=True, null=True)
    bafshgr   = models.CharField(blank=True, null=True) 
    year      = models.IntegerField(null=True, blank=True)   
 
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ba_fuel_type_emission_rate'
 
class BaFuelTypeGeneration(models.Model):
    id =  models.AutoField(primary_key=True) 
    bacode = models.ForeignKey(
        BalancingAuthority,
        on_delete=models.CASCADE,  # Deletes BAAnnualCombustion records if the related BalancingAuthority is deleted
        db_column='bacode'          # Ensures the column in the database is still named 'ba_id'
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


class BaNonBaseloadEmissionRate(models.Model):
    id       =  models.AutoField(primary_key=True) 
    bacode = models.ForeignKey(
        BalancingAuthority,
        on_delete=models.CASCADE,  # Deletes BAAnnualCombustion records if the related BalancingAuthority is deleted
        db_column='bacode'          # Ensures the column in the database is still named 'ba_id'
    )
    banbnox  = models.FloatField(null=True, blank=True)
    banbnxo  = models.FloatField(null=True, blank=True)
    banbso2  = models.FloatField(null=True, blank=True)
    banbco2  = models.FloatField(null=True, blank=True)
    banbch4  = models.FloatField(null=True, blank=True)
    banbn2o  = models.FloatField(null=True, blank=True)
    banbc2e  = models.FloatField(null=True, blank=True)
    banbhg   = models.FloatField(null=True, blank=True)
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
        db_table = 'ba_nonbaseload_emission_rate'

class BaResourceMix(models.Model):
    id       =  models.AutoField(primary_key=True) 
    bacode = models.ForeignKey(
        BalancingAuthority,
        on_delete=models.CASCADE,  # Deletes BAAnnualCombustion records if the related BalancingAuthority is deleted
        db_column='bacode'          # Ensures the column in the database is still named 'bacode'
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


class County(models.Model):  # TG: This needs to include fipsst as well since fipscnty can have duplicates across states
    cntyname = models.CharField(max_length=500, null=False, blank=False)
    fipscnty = models.CharField(max_length=500, null=False, blank=False)
    fipsst   = models.CharField(max_length=2)

    class Meta:
        db_table = 'county'
 
class Generator(models.Model):
    seqgen = models.FloatField(null=True, blank=True) 
    genid = models.CharField(null=True, blank=True)  
    orispl = models.IntegerField(null=False, blank=False)  
    # numblr   = models.FloatField(null=True, blank=True)
    # genstat  = models.CharField(max_length=500, null=True, blank=True)
    # prmvr    = models.CharField(max_length=500, null=True, blank=True)
    # fuelg1   = models.CharField(max_length=500, null=True, blank=True)
    # namepcap = models.FloatField(null=True, blank=True)
    # cfact    = models.FloatField(null=True, blank=True)
    # genntan  = models.FloatField(null=True, blank=True)
    # genntoz  = models.FloatField(null=True, blank=True)
    # genersrc = models.CharField(max_length=500, null=True, blank=True)
    # genyronl = models.FloatField(null=True, blank=True)
    # genyrret = models.FloatField(null=True, blank=True)
    # year = models.IntegerField(null=True, blank=True)  # Year
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'generator'

        constraints = [
            models.UniqueConstraint(fields=['genid', 'orispl'], name='unique_genid_orispl')
        ]
    

class NercRegion(models.Model):
    nerc = models.CharField(max_length=5, null=False, blank=False, unique=True)
    nerc_name = models.CharField(max_length=500, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'nerc_region'


class PlantDistributionSys(models.Model):
    oprcode = models.IntegerField(null=True, blank=True)
    oprname = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'plant_distribution_sys'

class PlantEmissionRate (models.Model):
    id = models.AutoField(primary_key=True) 
    orispl = models.ForeignKey(
                Plant,
                on_delete=models.CASCADE,  # Deletes PlantEmissionRate records if the related Plant is deleted
                db_column='orispl'          
            )
    plnoxrta = models.FloatField(blank=True, null=True)
    plnoxrto = models.FloatField(blank=True, null=True) 
    plso2rta = models.FloatField(blank=True, null=True)
    plco2rta = models.FloatField(blank=True, null=True)
    plch4rta = models.FloatField(blank=True, null=True)
    pln2orta = models.FloatField(blank=True, null=True)
    plc2erta = models.FloatField(blank=True, null=True)
    plhgrta  = models.CharField(blank=True, null=True) 
    plnoxra  = models.FloatField(blank=True, null=True)
    plnoxro  = models.FloatField(blank=True, null=True)
    plso2ra  = models.FloatField(blank=True, null=True)
    plco2ra  = models.FloatField(blank=True, null=True)
    plch4ra  = models.FloatField(blank=True, null=True)
    pln2ora  = models.FloatField(blank=True, null=True)
    plc2era  = models.FloatField(blank=True, null=True)
    plhgra   = models.CharField(blank=True, null=True) 
    plnoxcrt = models.FloatField(blank=True, null=True)
    plnoxcro = models.FloatField(blank=True, null=True)
    plso2crt = models.FloatField(blank=True, null=True)
    plco2crt = models.FloatField(blank=True, null=True)
    plch4crt = models.FloatField(blank=True, null=True)
    pln2ocrt = models.FloatField(blank=True, null=True)
    plc2ecrt = models.FloatField(blank=True, null=True)
    plhgcrt  = models.CharField(blank=True, null=True) 
    year     = models.IntegerField(null=True, blank=True)  # Year
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'plant_emission_rate'

class PlantFuelTypeGeneration (models.Model): 
    id = models.AutoField(primary_key=True) 
    orispl = models.ForeignKey(
                Plant,
                on_delete=models.CASCADE,  # Deletes PlantFuelTypeGeneration records if the related Plant is deleted
                db_column='orispl'          
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
    plgenaco = models.FloatField(blank=True, null=True)
    plgenatn = models.FloatField(null=True, blank=True) 
    plgenatr = models.FloatField(null=True, blank=True) 
    plgenato = models.FloatField(blank=True, null=True)
    plgenath = models.FloatField(null=True, blank=True) 
    year     = models.IntegerField(null=True, blank=True)  # Year
 
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'plant_fuel_type_generation'

class PlantResourceMix(models.Model):
    id = models.AutoField(primary_key=True) 
    orispl = models.ForeignKey(
                Plant,
                on_delete=models.CASCADE,  # Deletes plant_resource_mix records if the related Plant is deleted
                db_column='orispl'          
            )
    plclpr = models.FloatField(blank=True, null=True)
    plolpr = models.FloatField(blank=True, null=True)
    plgspr = models.FloatField(blank=True, null=True)
    plncpr = models.FloatField(blank=True, null=True)
    plhypr = models.FloatField(blank=True, null=True)
    plbmpr = models.FloatField(blank=True, null=True)
    plwipr = models.FloatField(blank=True, null=True)
    plsopr = models.FloatField(blank=True, null=True)
    plgtpr = models.FloatField(blank=True, null=True)
    plofpr = models.FloatField(blank=True, null=True)
    ploppr = models.FloatField(blank=True, null=True)
    pltnpr = models.FloatField(blank=True, null=True)
    pltrpr = models.FloatField(blank=True, null=True)
    pltopr = models.FloatField(blank=True, null=True)
    plthpr = models.FloatField(blank=True, null=True)
    plcypr = models.FloatField(blank=True, null=True)
    plcnpr = models.FloatField(blank=True, null=True)
    plcopr = models.FloatField(blank=True, null=True)
    year   = models.IntegerField(null=True, blank=True)  # Year
 
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'plant_resource_mix'


class Sector(models.Model):
    sector_id = models.AutoField(primary_key=True)  # do we want this auto generated / TG: Yes
    sector = models.CharField(max_length=500, null=False, blank=False)
   
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sector'

class State(models.Model):
    fipsst = models.CharField(max_length=500, null=False, blank=False, unique=True)
    pstatabb = models.CharField(max_length=2, null=False, blank=False)
   
    class Meta:
        db_table = 'state'


class StateAnnualCombustion(models.Model): 
    id     = models.AutoField(primary_key=True)
    fipsst = models.ForeignKey(
                State,
                on_delete=models.CASCADE,  # Deletes StateAnnualCombustion records if the related Plant is deleted
                db_column='fipsst'          
            )  
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
    sthgan     = models.FloatField(null=True, blank=True) 
    year       = models.IntegerField(null=True, blank=True)  
 
    class Meta:
        db_table = 'state_annual_combustion'

class Subregion(models.Model): 
    subrgn = models.CharField(primary_key=True, max_length=4, null=False, blank=False, unique=True)
    srname = models.CharField(max_length=255, null=False, blank=False)
     
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subregion'

class StateEmissionRate(models.Model):
    id = models.AutoField(primary_key=True)
    fipsst = models.ForeignKey(
                State,
                on_delete=models.CASCADE,  # Deletes StateAnnualCombustion records if the related Plant is deleted
                db_column='fipsst'          
            )  
    stnoxrta = models.FloatField(null=True, blank=True)
    stnoxrto = models.FloatField(null=True, blank=True)
    stso2rta = models.FloatField(null=True, blank=True)
    stco2rta = models.FloatField(null=True, blank=True)
    stch4rta = models.FloatField(null=True, blank=True)
    stn2orta = models.FloatField(null=True, blank=True)
    stc2erta = models.FloatField(null=True, blank=True)
    sthgrta  = models.CharField(null=True, blank=True)
    stnoxra  = models.FloatField(null=True, blank=True)
    stnoxro  = models.FloatField(null=True, blank=True)
    stso2ra  = models.FloatField(null=True, blank=True)
    stco2ra  = models.FloatField(null=True, blank=True)
    stch4ra  = models.FloatField(null=True, blank=True)
    stn2ora  = models.FloatField(null=True, blank=True)
    stc2era  = models.FloatField(null=True, blank=True)
    sthgra   = models.CharField(null=True, blank=True)
    stnoxcrt = models.FloatField(null=True, blank=True)
    stnoxcro = models.FloatField(null=True, blank=True)
    stso2crt = models.FloatField(null=True, blank=True)
    stco2crt = models.FloatField(null=True, blank=True)
    stch4crt = models.FloatField(null=True, blank=True)
    stn2ocrt = models.FloatField(null=True, blank=True)
    stc2ecrt = models.FloatField(null=True, blank=True)
    sthgcrt  = models.CharField(null=True, blank=True) 
    year     = models.IntegerField(null=True, blank=True)  

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'state_emission_rate'



class StateFuelTypeEmissionRate(models.Model): 
    id = models.AutoField(primary_key=True)
    fipsst = models.ForeignKey(
                State,
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
    stchgrt   = models.CharField(blank=True, null=True)
    stfshgrt  = models.CharField(blank=True, null=True)
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
    stchgr    = models.CharField(blank=True, null=True)
    stfshgr   = models.CharField(blank=True, null=True)
    year      = models.IntegerField(null=True, blank=True)  

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'state_fuel_type_emission_rate'


class StateFuelTypeGeneration(models.Model): 
    id = models.AutoField(primary_key=True)
    fipsst = models.ForeignKey(
                State,
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


class StateNonBaseloadEmissionRate(models.Model): 
    id = models.AutoField(primary_key=True)
    fipsst = models.ForeignKey(
                State,
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
    stnbhg   = models.FloatField(null=True, blank=True) 
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
        db_table = 'state_nonbaseload_emission_rate'

class StateResourceMix(models.Model): 
    id = models.AutoField(primary_key=True)
    fipsst = models.ForeignKey(
                State,
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

class SubrgnAnnualCombustion(models.Model): 
    id = models.AutoField(primary_key=True)
    subrgn = models.ForeignKey(
                Subregion,
                on_delete=models.CASCADE,  # Deletes SubrgnAnnualCombustion records if the related Plant is deleted
                db_column='subrgn'          
            ) 
    srhtian   = models.FloatField(null=True, blank=True)
    srhtioz   = models.FloatField(null=True, blank=True)
    srhtiant  = models.FloatField(null=True, blank=True)
    srhtiozt  = models.FloatField(null=True, blank=True)
    srngenan  = models.FloatField(null=True, blank=True)
    srngenoz  = models.FloatField(null=True, blank=True)
    srnoxan   = models.FloatField(null=True, blank=True)
    srnoxoz   = models.FloatField(null=True, blank=True)
    srso2an   = models.FloatField(null=True, blank=True)
    srco2an   = models.FloatField(null=True, blank=True)
    srch4an   = models.FloatField(null=True, blank=True)
    srn2oan   = models.FloatField(null=True, blank=True)
    srco2eqa  = models.FloatField(null=True, blank=True)
    srhgan    = models.FloatField(null=True, blank=True) 
    year      = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subrgn_annual_combustion'

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
    srhgrta  = models.CharField(blank=True, null=True)
    srnoxra  = models.FloatField(blank=True, null=True)
    srnoxro  = models.FloatField(blank=True, null=True)
    srso2ra  = models.FloatField(blank=True, null=True)
    srco2ra  = models.FloatField(blank=True, null=True)
    srch4ra  = models.FloatField(blank=True, null=True)
    srn2ora  = models.FloatField(blank=True, null=True)
    src2era  = models.FloatField(blank=True, null=True)
    srhgra   = models.CharField(blank=True, null=True)
    srnoxcrt = models.FloatField(blank=True, null=True)
    srnoxcro = models.FloatField(blank=True, null=True)
    srso2crt = models.FloatField(blank=True, null=True)
    srco2crt = models.FloatField(blank=True, null=True)
    srch4crt = models.FloatField(blank=True, null=True)
    srn2ocrt = models.FloatField(blank=True, null=True)
    src2ecrt = models.FloatField(blank=True, null=True)
    srhgcrt  = models.CharField(blank=True, null=True)
    year     = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subrgn_emission_rate'
  
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
    srchgrt   = models.CharField(blank=True, null=True)
    srfshgrt  = models.CharField(blank=True, null=True)
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
    srchgr    = models.CharField(blank=True, null=True)
    srfshgr   = models.CharField(blank=True, null=True)
    year      = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subrgn_fuel_type_emission_rate'

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
        db_column='orispl'          
    ) 
    prmvr = models.CharField(max_length=2, null=True, blank=True) 
    untopst = models.CharField(max_length=2, null=True, blank=True) 
    capdflag = models.CharField(max_length=50, null=True, blank=True)
    prgcode = models.CharField(max_length=4000, null=True, blank=True)
    botfirty = models.CharField(max_length=255, null=True, blank=True)
    numgen = models.IntegerField(null=True, blank=True)
    fuelu1 = models.CharField(max_length=6, null=True, blank=True)
    hrsop = models.FloatField(null=True, blank=True) 
    
    def __str__(self):
        return f"{self.unitid} - {self.orispl} - {self.prmvr}"

    class Meta:
        db_table = "unit"
        constraints = [
            models.UniqueConstraint(fields=["unitid", "orispl", "prmvr"], name="unit_composite_pk")
        ]
