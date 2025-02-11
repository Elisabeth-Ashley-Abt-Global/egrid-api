from django.db import models

class BalancingAuthority(models.Model): 
    bacode = models.CharField(max_length=7, primary_key=True, unique=True)  
    baname = models.CharField(max_length=255)   

    class Meta:
        db_table = "balancing_authority"

    def __str__(self):
        return self.name
    
class BAAnnualCombustion(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    bacode = models.ForeignKey(
        BalancingAuthority,
        on_delete=models.CASCADE,  # Deletes BAAnnualCombustion records if the related BalancingAuthority is deleted
        db_column='bacode'          # Ensures the column in the database is still named 'ba_id'
    )
    bahtian = models.FloatField(null=True, blank=True, db_comment='BA annual heat input from combustion (MMBtu)')  # BA annual heat input (MMBtu)
    bahtioz = models.FloatField(null=True, blank=True)
    bahtiant = models.FloatField(null=True, blank=True)
    bahtiozt = models.FloatField(null=True, blank=True)
    bangenan = models.FloatField(null=True, blank=True)
    bangenoz = models.FloatField(null=True, blank=True)
    banoxan = models.FloatField(null=True, blank=True)
    banoxoz = models.FloatField(null=True, blank=True)
    baso2an = models.FloatField(null=True, blank=True)
    baco2an = models.FloatField(null=True, blank=True)
    bach4an = models.FloatField(null=True, blank=True)
    ban2oan = models.FloatField(null=True, blank=True)
    baco2eqa = models.FloatField(null=True, blank=True)
    bahgan = models.FloatField(null=True, blank=True)  
    # created_on = models.DateTimeField(auto_now_add=True)  # Automatically sets the field to the current timestamp only when the record is first created.
    # updated_on = models.DateTimeField(auto_now=True) # Automatically updates the field to the current timestamp every time the record is saved.
    year = models.IntegerField(null=True, blank=True)  # Year
 
    class Meta:
        db_table = "ba_annual_combustion"

    def __str__(self):
        return self.name

class Plant(models.Model):
    seqplt = models.IntegerField(null=True, blank=True)
    orispl = models.IntegerField(null=False, blank=False, unique=True)  # Plant ID ADD A UNIQUE CONSTRAINT
    pstatabb = models.CharField(max_length=1000, null=True, blank=True)
    fipsst = models.CharField(max_length=1000, null=True, blank=True)  # State Id
    plant_name = models.CharField(max_length=1000, null=True, blank=True)
    oprcode = models.IntegerField(null=True, blank=True)
    utlsrvid = models.IntegerField(null=True, blank=True)
    sector_id = models.CharField(max_length=1000, null=True, blank=True)
    bacode = models.CharField(max_length=1000, null=True, blank=True)
    nerc = models.CharField(max_length=1000, null=True, blank=True)
    fipscnty = models.IntegerField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    numunt = models.IntegerField(null=True, blank=True)
    numgen = models.IntegerField(null=True, blank=True)
    plprmfl = models.CharField(max_length=1000, null=True, blank=True)
    plfuelct = models.CharField(max_length=1000, null=True, blank=True)
    coalflagind = models.CharField(max_length=1000, null=True, blank=True)
    subrgn = models.CharField(null=True, blank=True, max_length=4)
    year = models.IntegerField(null=True, blank=True)
    
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
    bahgrta  = models.FloatField(null=True, blank=True)
    banoxra  = models.FloatField(null=True, blank=True)
    banoxro  = models.FloatField(null=True, blank=True)
    baso2ra  = models.FloatField(null=True, blank=True)
    baco2ra  = models.FloatField(null=True, blank=True)
    bach4ra  = models.FloatField(null=True, blank=True)
    ban2ora  = models.FloatField(null=True, blank=True)
    bac2era  = models.FloatField(null=True, blank=True)
    bahgra   = models.FloatField(null=True, blank=True)
    banoxcrt = models.FloatField(null=True, blank=True)
    banoxcro = models.FloatField(null=True, blank=True)
    baso2crt = models.FloatField(null=True, blank=True)
    baco2crt = models.FloatField(null=True, blank=True)
    bach4crt = models.FloatField(null=True, blank=True)
    ban2ocrt = models.FloatField(null=True, blank=True)
    bac2ecrt = models.FloatField(null=True, blank=True)
    bahgcrt  = models.FloatField(null=True, blank=True)
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
    bacnoxrt = models.FloatField(null=True, blank=True)
    baonoxrt = models.FloatField(null=True, blank=True)
    bagnoxrt = models.FloatField(null=True, blank=True)
    bafsnxrt = models.FloatField(null=True, blank=True)
    bacnxort = models.FloatField(null=True, blank=True)
    baonxort = models.FloatField(null=True, blank=True)
    bagnxort = models.FloatField(null=True, blank=True)
    bafsnort = models.FloatField(null=True, blank=True)
    bacso2rt = models.FloatField(null=True, blank=True)
    baoso2rt = models.FloatField(null=True, blank=True)
    bagso2rt = models.FloatField(null=True, blank=True)
    bafss2rt = models.FloatField(null=True, blank=True)
    bacco2rt = models.FloatField(null=True, blank=True)
    baoco2rt = models.FloatField(null=True, blank=True)
    bagco2rt = models.FloatField(null=True, blank=True)
    bafsc2rt = models.FloatField(null=True, blank=True)
    bacch4rt = models.FloatField(null=True, blank=True)
    baoch4rt = models.FloatField(null=True, blank=True)
    bagch4rt = models.FloatField(null=True, blank=True)
    bafch4rt = models.FloatField(null=True, blank=True)
    bacn2ort = models.FloatField(null=True, blank=True)
    baon2ort = models.FloatField(null=True, blank=True)
    bagn2ort = models.FloatField(null=True, blank=True)
    bafn2ort = models.FloatField(null=True, blank=True)
    bacc2ert = models.FloatField(null=True, blank=True)
    baoc2ert = models.FloatField(null=True, blank=True)
    bagc2ert = models.FloatField(null=True, blank=True)
    bafsc2er = models.FloatField(null=True, blank=True)
    bachgrt  = models.FloatField(null=True, blank=True)
    bafshgrt = models.FloatField(null=True, blank=True)
    bacnoxr  = models.FloatField(null=True, blank=True)
    baonoxr  = models.FloatField(null=True, blank=True)
    bagnoxr  = models.FloatField(null=True, blank=True)
    bafsnxr  = models.FloatField(null=True, blank=True)
    bacnxor  = models.FloatField(null=True, blank=True)
    baonxor  = models.FloatField(null=True, blank=True)
    bagnxor  = models.FloatField(null=True, blank=True)
    bafsnor  = models.FloatField(null=True, blank=True)
    bacso2r  = models.FloatField(null=True, blank=True)
    baoso2r  = models.FloatField(null=True, blank=True)
    bagso2r  = models.FloatField(null=True, blank=True)
    bafss2r  = models.FloatField(null=True, blank=True)
    bacco2r  = models.FloatField(null=True, blank=True)
    baoco2r  = models.FloatField(null=True, blank=True)
    bagco2r  = models.FloatField(null=True, blank=True)
    bafsc2r  = models.FloatField(null=True, blank=True)
    bacch4r  = models.FloatField(null=True, blank=True)
    baoch4r  = models.FloatField(null=True, blank=True)
    bagch4r  = models.FloatField(null=True, blank=True)
    bafch4r  = models.FloatField(null=True, blank=True)
    bacn2or  = models.FloatField(null=True, blank=True)
    baon2or  = models.FloatField(null=True, blank=True)
    bagn2or  = models.FloatField(null=True, blank=True)
    bafn2or  = models.FloatField(null=True, blank=True)
    bacc2er  = models.FloatField(null=True, blank=True)
    baoc2er  = models.FloatField(null=True, blank=True)
    bagc2er  = models.FloatField(null=True, blank=True)
    bafsc2er = models.FloatField(null=True, blank=True)
    bachgr   = models.FloatField(null=True, blank=True)
    bafshgr  = models.FloatField(null=True, blank=True) 
    year = models.IntegerField(null=True, blank=True)   
 
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
    bagenacl = models.FloatField(null=True, blank=True)
    bagenaol = models.FloatField(null=True, blank=True)
    bagenags = models.FloatField(null=True, blank=True)
    bagenanc = models.FloatField(null=True, blank=True)
    bagenahy = models.FloatField(null=True, blank=True)
    bagenabm = models.FloatField(null=True, blank=True)
    bagenawi = models.FloatField(null=True, blank=True)
    bagenaso = models.FloatField(null=True, blank=True)
    bagenagt = models.FloatField(null=True, blank=True)
    bagenaof = models.FloatField(null=True, blank=True)
    bagenaop = models.FloatField(null=True, blank=True)
    bagenatn = models.FloatField(null=True, blank=True)
    bagenatr = models.FloatField(null=True, blank=True)
    bagenath = models.FloatField(null=True, blank=True)
    bagenacy = models.FloatField(null=True, blank=True)
    bagenacn = models.FloatField(null=True, blank=True)
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
    baclpr = models.FloatField(null=True, blank=True)
    baolpr = models.FloatField(null=True, blank=True)
    bagspr = models.FloatField(null=True, blank=True)
    bancpr = models.FloatField(null=True, blank=True)
    bahypr = models.FloatField(null=True, blank=True)
    babmpr = models.FloatField(null=True, blank=True)
    bawipr = models.FloatField(null=True, blank=True)
    basopr = models.FloatField(null=True, blank=True)
    bagtpr = models.FloatField(null=True, blank=True)
    baofpr = models.FloatField(null=True, blank=True)
    baoppr = models.FloatField(null=True, blank=True)
    batnpr = models.FloatField(null=True, blank=True)
    batrpr = models.FloatField(null=True, blank=True)
    bathpr = models.FloatField(null=True, blank=True)
    bacypr = models.FloatField(null=True, blank=True)
    bacnpr = models.FloatField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)  

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ba_resource_mix'


class County(models.Model):
    cntyname = models.CharField(max_length=500, null=False, blank=False)
    fipscnty =  models.CharField(max_length=500, null=False, blank=False)

    class Meta:
        db_table = 'county'
 
class Generator(models.Model):
    seqgen = models.FloatField(null=True, blank=True) 
    genid = models.CharField(null=True, blank=True) 
    orispl = models.ForeignKey(
                Plant,
                on_delete=models.CASCADE,  # Deletes Generator records if the related Plant is deleted
                db_column='orispl'          
            )
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
    plnoxrta = models.FloatField(null=True, blank=True)
    plnoxra  = models.FloatField(null=True, blank=True)
    plnoxro  = models.FloatField(null=True, blank=True)
    plso2ra  = models.FloatField(null=True, blank=True)
    plco2ra  = models.FloatField(null=True, blank=True)
    plch4ra  = models.FloatField(null=True, blank=True)
    pln2ora  = models.FloatField(null=True, blank=True)
    plc2era  = models.FloatField(null=True, blank=True)
    plhgra   = models.FloatField(null=True, blank=True)
    plnoxcrt = models.FloatField(null=True, blank=True)
    plnoxcro = models.FloatField(null=True, blank=True)
    plso2crt = models.FloatField(null=True, blank=True)
    plco2crt = models.FloatField(null=True, blank=True)
    plch4crt = models.FloatField(null=True, blank=True)
    pln2ocrt = models.FloatField(null=True, blank=True)
    plc2ecrt = models.FloatField(null=True, blank=True)
    plhgcrt  = models.FloatField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)  # Year
    
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
    plgenatn = models.FloatField(null=True, blank=True) 
    plgenatr = models.FloatField(null=True, blank=True) 
    plgenath = models.FloatField(null=True, blank=True) 
    year = models.IntegerField(null=True, blank=True)  # Year
 
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
    plclpr     = models.FloatField(null=True, blank=True)
    plolpr     = models.FloatField(null=True, blank=True)
    plgspr     = models.FloatField(null=True, blank=True)
    plncpr     = models.FloatField(null=True, blank=True)
    plhypr     = models.FloatField(null=True, blank=True)
    plbmpr     = models.FloatField(null=True, blank=True)
    plwipr     = models.FloatField(null=True, blank=True)
    plsopr     = models.FloatField(null=True, blank=True)
    plgtpr     = models.FloatField(null=True, blank=True)
    plofpr     = models.FloatField(null=True, blank=True)
    ploppr     = models.FloatField(null=True, blank=True) 
    year       = models.IntegerField(null=True, blank=True)  # Year
 
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'plant_resource_mix'


class Sector(models.Model):
    sector_id = models.AutoField(primary_key=True)  # do we want this auto generated
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
    sthgrta  = models.FloatField(null=True, blank=True)
    stnoxra  = models.FloatField(null=True, blank=True)
    stnoxro  = models.FloatField(null=True, blank=True)
    stso2ra  = models.FloatField(null=True, blank=True)
    stco2ra  = models.FloatField(null=True, blank=True)
    stch4ra  = models.FloatField(null=True, blank=True)
    stn2ora  = models.FloatField(null=True, blank=True)
    stc2era  = models.FloatField(null=True, blank=True)
    sthgra   = models.FloatField(null=True, blank=True)
    stnoxcrt = models.FloatField(null=True, blank=True)
    stnoxcro = models.FloatField(null=True, blank=True)
    stso2crt = models.FloatField(null=True, blank=True)
    stco2crt = models.FloatField(null=True, blank=True)
    stch4crt = models.FloatField(null=True, blank=True)
    stn2ocrt = models.FloatField(null=True, blank=True)
    stc2ecrt = models.FloatField(null=True, blank=True)
    sthgcrt  = models.FloatField(null=True, blank=True) 
    year       = models.IntegerField(null=True, blank=True)  

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
    stcnoxrt = models.FloatField(null=True, blank=True)
    stonoxrt = models.FloatField(null=True, blank=True)
    stgnoxrt = models.FloatField(null=True, blank=True)
    stfsnxrt = models.FloatField(null=True, blank=True)
    stcnxort = models.FloatField(null=True, blank=True)
    stonxort = models.FloatField(null=True, blank=True)
    stgnxort = models.FloatField(null=True, blank=True)
    stfsnort = models.FloatField(null=True, blank=True)
    stcso2rt = models.FloatField(null=True, blank=True)
    stoso2rt = models.FloatField(null=True, blank=True)
    stgso2rt = models.FloatField(null=True, blank=True)
    stfss2rt = models.FloatField(null=True, blank=True)
    stcco2rt = models.FloatField(null=True, blank=True)
    stoco2rt = models.FloatField(null=True, blank=True)
    stgco2rt = models.FloatField(null=True, blank=True)
    stfsc2rt = models.FloatField(null=True, blank=True)
    stcch4rt = models.FloatField(null=True, blank=True)
    stoch4rt = models.FloatField(null=True, blank=True)
    stgch4rt = models.FloatField(null=True, blank=True)
    stfch4rt = models.FloatField(null=True, blank=True)
    stcn2ort = models.FloatField(null=True, blank=True)
    ston2ort = models.FloatField(null=True, blank=True)
    stgn2ort = models.FloatField(null=True, blank=True)
    stfn2ort = models.FloatField(null=True, blank=True)
    stcc2ert = models.FloatField(null=True, blank=True)
    stoc2ert = models.FloatField(null=True, blank=True)
    stgc2ert = models.FloatField(null=True, blank=True)
    stfsc2ert = models.FloatField(null=True, blank=True)
    stchgrt  = models.FloatField(null=True, blank=True)
    stfshgrt = models.FloatField(null=True, blank=True)
    stcnoxr  = models.FloatField(null=True, blank=True)
    stonoxr  = models.FloatField(null=True, blank=True)
    stgnoxr  = models.FloatField(null=True, blank=True)
    stfsnxr  = models.FloatField(null=True, blank=True)
    stcnxor  = models.FloatField(null=True, blank=True)
    stonxor  = models.FloatField(null=True, blank=True)
    stgnxor  = models.FloatField(null=True, blank=True)
    stfsnor  = models.FloatField(null=True, blank=True)
    stcso2r  = models.FloatField(null=True, blank=True)
    stoso2r  = models.FloatField(null=True, blank=True)
    stgso2r  = models.FloatField(null=True, blank=True)
    stfss2r  = models.FloatField(null=True, blank=True)
    stcco2r  = models.FloatField(null=True, blank=True)
    stoco2r  = models.FloatField(null=True, blank=True)
    stgco2r  = models.FloatField(null=True, blank=True)
    stfsc2r  = models.FloatField(null=True, blank=True)
    stcch4r  = models.FloatField(null=True, blank=True)
    stoch4r  = models.FloatField(null=True, blank=True)
    stgch4r  = models.FloatField(null=True, blank=True)
    stfch4r  = models.FloatField(null=True, blank=True)
    stcn2or  = models.FloatField(null=True, blank=True)
    ston2or  = models.FloatField(null=True, blank=True)
    stgn2or  = models.FloatField(null=True, blank=True)
    stfn2or  = models.FloatField(null=True, blank=True)
    stcc2er  = models.FloatField(null=True, blank=True)
    stoc2er  = models.FloatField(null=True, blank=True)
    stgc2er  = models.FloatField(null=True, blank=True)
    stfsc2er = models.FloatField(null=True, blank=True)
    stchgr   = models.FloatField(null=True, blank=True)
    stfshgr  = models.FloatField(null=True, blank=True) 
    year       = models.IntegerField(null=True, blank=True)  

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
    stgenacl = models.FloatField(null=True, blank=True)
    stgenaol = models.FloatField(null=True, blank=True)
    stgenaso = models.FloatField(null=True, blank=True)
    stgenagt = models.FloatField(null=True, blank=True)
    stgenaof = models.FloatField(null=True, blank=True)
    stgenaop = models.FloatField(null=True, blank=True)
    stgenatn = models.FloatField(null=True, blank=True)
    stgenatr = models.FloatField(null=True, blank=True)
    stgenath = models.FloatField(null=True, blank=True)
    stgenacy = models.FloatField(null=True, blank=True)
    stgenacn = models.FloatField(null=True, blank=True)
    stgenags = models.FloatField(null=True, blank=True)
    stgenanc = models.FloatField(null=True, blank=True)
    stgenahy = models.FloatField(null=True, blank=True)
    stgenabm = models.FloatField(null=True, blank=True)
    stgenawi = models.FloatField(null=True, blank=True) 
    year       = models.IntegerField(null=True, blank=True)  

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
    stclpr = models.FloatField(null=True, blank=True) 
    stolpr = models.FloatField(null=True, blank=True) 
    stgspr = models.FloatField(null=True, blank=True) 
    stncpr = models.FloatField(null=True, blank=True) 
    sthypr = models.FloatField(null=True, blank=True) 
    stbmpr = models.FloatField(null=True, blank=True) 
    stwipr = models.FloatField(null=True, blank=True) 
    stsopr = models.FloatField(null=True, blank=True) 
    stgtpr = models.FloatField(null=True, blank=True) 
    stofpr = models.FloatField(null=True, blank=True) 
    stoppr = models.FloatField(null=True, blank=True) 
    sttnpr = models.FloatField(null=True, blank=True) 
    sttrpr = models.FloatField(null=True, blank=True) 
    stthpr = models.FloatField(null=True, blank=True) 
    stcypr = models.FloatField(null=True, blank=True) 
    stcnpr = models.FloatField(null=True, blank=True)  
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
    year   = models.IntegerField(null=True, blank=True)

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
    srnoxrta = models.FloatField(null=True, blank=True)
    srnoxrto = models.FloatField(null=True, blank=True)
    srso2rta = models.FloatField(null=True, blank=True)
    srco2rta = models.FloatField(null=True, blank=True)
    srch4rta = models.FloatField(null=True, blank=True)
    srn2orta = models.FloatField(null=True, blank=True)
    src2erta = models.FloatField(null=True, blank=True)
    srhgrta  = models.FloatField(null=True, blank=True)
    srnoxra  = models.FloatField(null=True, blank=True)
    srnoxro  = models.FloatField(null=True, blank=True)
    srso2ra  = models.FloatField(null=True, blank=True)
    srco2ra  = models.FloatField(null=True, blank=True)
    srch4ra  = models.FloatField(null=True, blank=True)
    srn2ora  = models.FloatField(null=True, blank=True)
    src2era  = models.FloatField(null=True, blank=True)
    srhgra   = models.FloatField(null=True, blank=True)
    srnoxcrt = models.FloatField(null=True, blank=True)
    srnoxcro = models.FloatField(null=True, blank=True)
    srso2crt = models.FloatField(null=True, blank=True)
    srco2crt = models.FloatField(null=True, blank=True)
    srch4crt = models.FloatField(null=True, blank=True)
    srn2ocrt = models.FloatField(null=True, blank=True)
    src2ecrt = models.FloatField(null=True, blank=True)
    srhgcrt  = models.FloatField(null=True, blank=True) 
    year   = models.IntegerField(null=True, blank=True)

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
    sronxort = models.FloatField(null=True, blank=True)
    srgnxort = models.FloatField(null=True, blank=True)
    srfsnort = models.FloatField(null=True, blank=True)
    srcso2rt = models.FloatField(null=True, blank=True)
    sroso2rt = models.FloatField(null=True, blank=True)
    srgso2rt = models.FloatField(null=True, blank=True)
    srfss2rt = models.FloatField(null=True, blank=True)
    srcco2rt = models.FloatField(null=True, blank=True)
    sroco2rt = models.FloatField(null=True, blank=True)
    srgco2rt = models.FloatField(null=True, blank=True)
    srfsc2rt = models.FloatField(null=True, blank=True)
    srcch4rt = models.FloatField(null=True, blank=True)
    sroch4rt = models.FloatField(null=True, blank=True)
    srgch4rt = models.FloatField(null=True, blank=True)
    srfch4rt = models.FloatField(null=True, blank=True)
    srcn2ort = models.FloatField(null=True, blank=True)
    sron2ort = models.FloatField(null=True, blank=True)
    srgn2ort = models.FloatField(null=True, blank=True)
    srfn2ort = models.FloatField(null=True, blank=True)
    srcc2ert = models.FloatField(null=True, blank=True)
    sroc2ert = models.FloatField(null=True, blank=True)
    srgc2ert = models.FloatField(null=True, blank=True)
    srfsc2ert= models.FloatField(null=True, blank=True)
    srchgrt  = models.FloatField(null=True, blank=True)
    srfshgrt = models.FloatField(null=True, blank=True)
    srcnoxr  = models.FloatField(null=True, blank=True)
    sronoxr  = models.FloatField(null=True, blank=True)
    srgnoxr  = models.FloatField(null=True, blank=True)
    srfsnxr  = models.FloatField(null=True, blank=True)
    srcnxor  = models.FloatField(null=True, blank=True)
    sronxor  = models.FloatField(null=True, blank=True)
    srgnxor  = models.FloatField(null=True, blank=True)
    srfsnor  = models.FloatField(null=True, blank=True)
    srcso2r  = models.FloatField(null=True, blank=True)
    sroso2r  = models.FloatField(null=True, blank=True)
    srgso2r  = models.FloatField(null=True, blank=True)
    srfss2r  = models.FloatField(null=True, blank=True)
    srcco2r  = models.FloatField(null=True, blank=True)
    sroco2r  = models.FloatField(null=True, blank=True)
    srgco2r  = models.FloatField(null=True, blank=True)
    srfsc2r  = models.FloatField(null=True, blank=True)
    srcch4r  = models.FloatField(null=True, blank=True)
    sroch4r  = models.FloatField(null=True, blank=True)
    srgch4r  = models.FloatField(null=True, blank=True)
    srfch4r  = models.FloatField(null=True, blank=True)
    srcn2or  = models.FloatField(null=True, blank=True)
    sron2or  = models.FloatField(null=True, blank=True)
    srgn2or  = models.FloatField(null=True, blank=True)
    srfn2or  = models.FloatField(null=True, blank=True)
    srcc2er  = models.FloatField(null=True, blank=True)
    sroc2er  = models.FloatField(null=True, blank=True)
    srgc2er  = models.FloatField(null=True, blank=True)
    srfsc2er = models.FloatField(null=True, blank=True)
    srchgr   = models.FloatField(null=True, blank=True)
    srfshgr = models.FloatField(null=True, blank=True)
    year   = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subrgn_fuel_type_emission_rate'

class Utility(models.Model):
    utlsrvid = models.IntegerField(primary_key=True, unique=True)
    utlsrvnm = models.CharField(max_length=500, null=False, blank=False)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'utility'
