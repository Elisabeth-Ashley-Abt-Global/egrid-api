# File to communicate with the R API
import requests  
import logging
import pandas as pd  
from sqlalchemy import text 
from .utils import update_from_temp_table, build_insert_from_temp_sql

logger = logging.getLogger('egrid')
  
def populate_balancing_auth_data(engine=None, api_url=None):
    print("*populate_balancing_auth_data")
 
    try:
        response = requests.get(f"{api_url}balancingauthority")
        data = response.json() 
        # print(data) 
        
        if response.status_code == 200 and data.get('success'):
            ba_data = data.get('data', [])
            df = pd.DataFrame(ba_data) 

            cast_to_int = ['year']
            cast_to_float = ['bahtian', 'bahtioz', 'bahtiant', 'banamepcap',
                              'bahtiozt', 'bangenan', 'bangenoz', 'banoxan', 'banoxoz', 
                              'baso2an', 'baco2an', 'bach4an', 'ban2oan', 'baco2eqa', 'bahgan',
                              'banoxrta','banoxrto' ,'baso2rta' ,'baco2rta' ,'bach4rta' ,'ban2orta','bac2erta',
                              'banoxra','banoxro' ,'baso2ra' ,'baco2ra' ,'bach4ra' ,'ban2ora' ,'bac2era',
                              'banoxcrt','banoxcro','baso2crt','baco2crt', 'bach4crt', 'ban2ocrt', 'bac2ecrt', 'bahgcrt',
                              'bacnoxrt','baonoxrt','bagnoxrt','bafsnxrt','bacnxort','baonxort','bagnxort','bafsnort','bacso2rt',
                              'baoso2rt','bagso2rt','bafss2rt','bacco2rt','baoco2rt','bagco2rt','bafsc2rt','bacch4rt','baoch4rt',
                              'bagch4rt','bafch4rt','bacn2ort','baon2ort','bagn2ort','bafn2ort','bacc2ert','baoc2ert','bagc2ert',
                              'bafsc2er'  ,'bacnoxr','baonoxr','bagnoxr','bafsnxr','bacnxor','baonxor','bagnxor','bafsnor',
                              'bacso2r','baoso2r' ,'bagso2r','bafss2r','bacco2r','baoco2r','bagco2r','bafsc2r','bacch4r',
                              'baoch4r','bagch4r','bafch4r','bacn2or','baon2or','bagn2or','bafn2or','bacc2er','baoc2er',
                              'bagc2er','bafsc2er']
            
            for col in cast_to_int:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(int)

            for col in cast_to_float:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
 

            year = df['year'].unique()[0] 
            print('year ', year)

            ba_df = df[['bacode', 'baname', 'banamepcap']] 

            # baadjustedvalues_df
            baadjustedvalues_df = df[['bacode', 'year', 'bahtian', 'bahtioz', 'bahtiant', 'bahtiozt', 'bangenan', 'bangenoz', 'banoxan', 'banoxoz', 'baso2an', 'baco2an', 'bach4an', 'ban2oan', 'baco2eqa', 'bahgan']]
            baadjustedvalues_df = baadjustedvalues_df.copy()
            baadjustedvalues_df.replace({"--": None, "N/A": None, "": None}, inplace=True) # replace placeholders else you'll encounter  invalid input syntax for type double precision

            #  TEST
            # update_row_from_df(
            #     conn=conn,
            #     table="ba_adjusted_values",
            #     df=baadjustedvalues_df,
            #     where_col="id",
            #     where_val=1
            # )
           
            # BaEmissionRate
            try:  
                baemissionrate_df = df[['bacode', 'year', 'banoxrta','banoxrto','baso2rta','baco2rta','bach4rta', 'ban2orta' ,'bac2erta','bahgrta','banoxra',
                                     'banoxro','baso2ra', 'baco2ra','bach4ra','ban2ora','bac2era','bahgra','banoxcrt','banoxcro','baso2crt','baco2crt', 'bach4crt', 'ban2ocrt', 'bahgcrt', 'bac2ecrt']] # field:  'bac2ecrt' is failing
                baemissionrate_df = baemissionrate_df.copy()
                baemissionrate_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception:
                print('Error in BaEmissionRate dataframe')
 
            try: 
                bafueltypeemissionrate_df = df[['bacode', 'year', 'bacnoxrt','baonoxrt','bagnoxrt','bafsnxrt','bacnxort','baonxort','bagnxort',             
                'bafsnort','bacso2rt','baoso2rt','bagso2rt','bafss2rt',  
                'bacco2rt','baoco2rt','bagco2rt','bafsc2rt','bacch4rt','baoch4rt','bagch4rt',
                'bafch4rt','bacn2ort','baon2ort','bagn2ort','bafn2ort','bacc2ert','baoc2ert','bagc2ert','bafsc2ert','bachgrt','bafshgrt',
                'bacnoxr','baonoxr','bagnoxr','bafsnxr','bacnxor','baonxor','bagnxor','bafsnor','bacso2r','baoso2r','bagso2r','bafss2r','bacco2r',
                'baoco2r','bagco2r','bafsc2r','bacch4r','baoch4r','bagch4r','bafch4r','bacn2or','baon2or','bagn2or','bafn2or','bacc2er','baoc2er','bagc2er',
                'bafsc2er','bachgr','bafshgr']]

                bafueltypeemissionrate_df = bafueltypeemissionrate_df.copy()
                bafueltypeemissionrate_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception:
                print('Error in bafueltypeemissionrate_df dataframe')

        
            try:

                ba_df.to_sql('balancing_authority_temp', con=engine, if_exists='replace', index=False) 
                baadjustedvalues_df.to_sql('ba_adjusted_values_temp', con=engine, if_exists='replace', index=False)
                baemissionrate_df.to_sql('ba_emission_rate_temp', con=engine, if_exists='replace', index=False)
                bafueltypeemissionrate_df.to_sql('ba_fuel_type_emission_rate_temp', con=engine, if_exists='replace', index=False)
                
                with engine.connect() as conn:
                    trans = conn.begin()
                    ba_cnt = conn.execute(text("select count(*) from balancing_authority;")).scalar()
                    
                    baadjustedvalues_cnt = conn.execute(
                        text("select count(*) from ba_adjusted_values where year = :year"),
                        {"year": int(year)}
                    ).scalar()  

                    ba_fuel_type_emission_rate_cnt = conn.execute(
                        text("select count(*) from ba_fuel_type_emission_rate where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    baemissionrate_cnt = conn.execute(
                        text("select count(*) from ba_emission_rate where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    if ba_cnt == 0:
                        conn.execute(text("""
                            insert into balancing_authority (
                                bacode, baname, banamepcap
                            ) select bacode, baname, banamepcap 
                            from balancing_authority_temp;
                        """))
                    else:
                        conn.execute(text("""
                            update balancing_authority 
                            set bacode = bt.bacode, 
                                baname = bt.baname,
                                banamepcap = bt.banamepcap              
                            from balancing_authority_temp bt
                            where balancing_authority.bacode = bt.bacode;
                        """))

                    # if baadjustedvalues_cnt == 0:
                    #     try:
                    #         conn.execute(text("""insert into ba_adjusted_values (
                    #                                 bacode, year, bahtian, bahtioz, bahtiant, bahtiozt,
                    #                                 bangenan, bangenoz, banoxan, banoxoz, baso2an,
                    #                                 baco2an, bach4an, ban2oan, baco2eqa, bahgan
                    #                             ) select bacode, year, bahtian, bahtioz, bahtiant, bahtiozt,
                    #                                 bangenan, bangenoz, banoxan, banoxoz, baso2an,
                    #                                 baco2an, bach4an, ban2oan, baco2eqa, bahgan 
                    #                             from ba_adjusted_values_temp;"""))
                    #     except Exception as e:
                    #         print('Error inserting into ba_adjusted_values', e)
                    #         return {"error": str(e)}
                    # else:
                    #     # conn.execute(text("""update ba_adjusted_values  
                    #     #                     set bacode = b.bacode,
                    #     #                     year = b.year,
                    #     #                     bahtian = b.bahtian,
                    #     #                     bahtioz = b.bahtioz,
                    #     #                     bahtiant = b.bahtiant,
                    #     #                     bahtiozt = b.bahtiozt,
                    #     #                     bangenan = b.bangenan,
                    #     #                     bangenoz = b.bangenoz,
                    #     #                     banoxan = b.banoxan,
                    #     #                     banoxoz = b.banoxoz,
                    #     #                     baso2an = b.baso2an,
                    #     #                     baco2an = b.baco2an,
                    #     #                     bach4an = b.bach4an,
                    #     #                     ban2oan = b.ban2oan,
                    #     #                     baco2eqa = b.baco2eqa,
                    #     #                     bahgan = b.bahgan
                    #     #                     from ba_adjusted_values_temp b
                    #     #                     where ba_adjusted_values.bacode = b.bacode
                    #     #                     and ba_adjusted_values.year = b.year;"""))
                    #     # test
                       
                        # sql = update_from_temp_table( "ba_adjusted_values", baadjustedvalues_df)
                        # conn.execute(text(sql))    

                    if baemissionrate_cnt == 0:
                        # conn.execute(text("""insert into ba_emission_rate (
                        #     bacode
                        #     ,banoxrta
                        #     ,banoxrto
                        #     ,baso2rta
                        #     ,baco2rta
                        #     ,bach4rta
                        #     ,ban2orta
                        #     ,bac2erta
                        #     ,bahgrta 
                        #     ,banoxra 
                        #     ,banoxro 
                        #     ,baso2ra 
                        #     ,baco2ra 
                        #     ,bach4ra 
                        #     ,ban2ora 
                        #     ,bac2era 
                        #     ,bahgra  
                        #     ,banoxcrt
                        #     ,banoxcro
                        #     ,baso2crt
                        #     ,baco2crt
                        #     ,bach4crt
                        #     ,ban2ocrt
                        #     ,bac2ecrt
                        #     ,bahgcrt  
                        # ) select 
                        #     bacode
                        #     ,banoxrta
                        #     ,banoxrto
                        #     ,baso2rta
                        #     ,baco2rta
                        #     ,bach4rta
                        #     ,ban2orta
                        #     ,bac2erta
                        #     ,bahgrta 
                        #     ,banoxra 
                        #     ,banoxro 
                        #     ,baso2ra 
                        #     ,baco2ra 
                        #     ,bach4ra 
                        #     ,ban2ora 
                        #     ,bac2era 
                        #     ,bahgra  
                        #     ,banoxcrt
                        #     ,banoxcro
                        #     ,baso2crt
                        #     ,baco2crt
                        #     ,bach4crt
                        #     ,ban2ocrt
                        #     ,bac2ecrt
                        #     ,bahgcrt from ba_emission_rate_temp;""")) 

                        sql = build_insert_from_temp_sql("ba_emission_rate", baemissionrate_df)
                        conn.execute(text(sql))  
                    else:
                        # conn.execute(text("""update ba_emission_rate  
                        #                     set bacode = b.bacode,
                        #                         banoxrta = b.banoxrta,
                        #                         banoxrto = b.banoxrto,
                        #                         baso2rta = b.baso2rta,
                        #                         baco2rta = b.baco2rta,
                        #                         bach4rta = b.bach4rta,
                        #                         ban2orta = b.ban2orta,
                        #                         bac2erta = b.bac2erta,
                        #                         bahgrta = b.bahgrta,
                        #                         banoxra = b.banoxra,
                        #                         banoxro = b.banoxro,
                        #                         baso2ra = b.baso2ra,
                        #                         baco2ra = b.baco2ra,
                        #                         bach4ra = b.bach4ra,
                        #                         ban2ora = b.ban2ora,
                        #                         bac2era = b.bac2era,
                        #                         bahgra = b.bahgra
                        #                     from ba_emission_rate_temp b
                        #                     where ba_emission_rate.bacode = b.bacode
                        #                     and ba_emission_rate.year = b.year;"""))
                        sql = update_from_temp_table("ba_emission_rate", baemissionrate_df)
                        conn.execute(text(sql))  
 
                    # if ba_fuel_type_emission_rate_cnt == 0:
                    #     conn.execute(text("""insert into ba_fuel_type_emission_rate (
                    #         bacode, year, bacnoxrt,baonoxrt,bagnoxrt,bafsnxrt,bacnxort,baonxort,bagnxort,             
                    #         bafsnort,bacso2rt,baoso2rt,bagso2rt,bafss2rt,  
                    #         bacco2rt,baoco2rt,bagco2rt,bafsc2rt,bacch4rt,baoch4rt,bagch4rt,
                    #         bafch4rt,bacn2ort,baon2ort,bagn2ort,bafn2ort,bacc2ert,baoc2ert,bagc2ert,bafsc2ert,bachgrt,bafshgrt,
                    #         bacnoxr,baonoxr,bagnoxr,bafsnxr,bacnxor,baonxor,bagnxor,bafsnor,bacso2r,baoso2r,bagso2r,bafss2r,bacco2r,
                    #         baoco2r,bagco2r,bafsc2r,bacch4r,baoch4r,bagch4r,bafch4r,bacn2or,baon2or,bagn2or,bafn2or,bacc2er,baoc2er,bagc2er,
                    #         bafsc2er,bachgr,bafshgr)
                    #     select bacode, year, bacnoxrt,baonoxrt,bagnoxrt,bafsnxrt,bacnxort,baonxort,bagnxort,             
                    #         bafsnort,bacso2rt,baoso2rt,bagso2rt,bafss2rt,  
                    #         bacco2rt,baoco2rt,bagco2rt,bafsc2rt,bacch4rt,baoch4rt,bagch4rt,
                    #         bafch4rt,bacn2ort,baon2ort,bagn2ort,bafn2ort,bacc2ert,baoc2ert,bagc2ert,bafsc2ert,bachgrt,bafshgrt,
                    #         bacnoxr,baonoxr,bagnoxr,bafsnxr,bacnxor,baonxor,bagnxor,bafsnor,bacso2r,baoso2r,bagso2r,bafss2r,bacco2r,
                    #         baoco2r,bagco2r,bafsc2r,bacch4r,baoch4r,bagch4r,bafch4r,bacn2or,baon2or,bagn2or,bafn2or,bacc2er,baoc2er,bagc2er,
                    #         bafsc2er,bachgr,bafshgr from ba_fuel_type_emission_rate_temp;"""))
                    # else:   
                    #     conn.execute(text("""update ba_fuel_type_emission_rate
                    #                         set bacode = b.bacode,
                    #                             year = b.year,
                    #                             bacnoxrt = b.bacnoxrt,
                    #                             baonoxrt = b.baonoxrt,
                    #                             bagnoxrt = b.bagnoxrt,
                    #                             bafsnxrt = b.bafsnxrt,
                    #                             bacnxort = b.bacnxort,
                    #                             baonxort = b.baonxort,
                    #                             bagnxort = b.bagnxort,
                    #                             bafsnort = b.bafsnort,
                    #                             bacso2rt = b.bacso2rt,
                    #                             baoso2rt = b.baoso2rt,
                    #                             bagso2rt = b.bagso2rt,
                    #                             bafss2rt = b.bafss2rt,
                    #                             bacco2rt = b.bacco2rt,
                    #                             baoco2rt = b.baoco2rt,
                    #                             bagco2rt = b.bagco2rt,
                    #                             bafsc2rt = b.bafsc2rt,
                    #                             bacch4rt = b.bacch4rt,
                    #                             baoch4rt = b.baoch4rt,
                    #                             bagch4rt = b.bagch4rt,
                    #                             bafch4rt = b.bafch4rt,
                    #                             bacn2ort = b.bacn2ort,
                    #                             baon2ort = b.baon2ort,
                    #                             bagn2ort = b.bagn2ort,
                    #                             bafn2ort = b.bafn2ort,
                    #                             bacc2ert = b.bacc2ert,
                    #                             baoc2ert = b.baoc2ert,
                    #                             bagc2ert = b.bagc2ert, 
                    #                             bafsc2er  =b.bafsc2er, 
                    #                             bachgrt  = b.bachgrt, 
                    #                             bafshgrt  = b.bafshgrt,
                    #                             bacnoxr = b.bacnoxr,
                    #                             baonoxr = b.baonoxr,
                    #                             bagnoxr = b.bagnoxr,
                    #                          bafsnxr,
                    #                       bacnxor,
                    #                       baonxor,
                    #                       bagnxor,
                    #                       bafsnor,
                    #                       bacso2r,
                    #                       baoso2r,
                    #                       bagso2r,
                    #                       bafss2r,
                    #                       bacco2r,
                    #                      baoco2r,
                    #                       bagco2r,
                    #                       bafsc2r,
                    #                       bacch4r,
                    #                       baoch4r,
                    #                       bagch4r,
                    #                       bafch4r,
                    #                       bacn2or,
                    #                       baon2or,
                    #                       bagn2or,
                    #                       bafn2or,
                    #                       bacc2er,
                    #                       baoc2er,
                    #                       bagc2er,
                    #                         bafsc2er,
                    #                       bachgr,bafshgr  
                                                        
                    #                         where ba_fuel_type_emission_rate.bacode = b.bacode
                    #                         and ba_fuel_type_emission_rate.year = b.year;"""))
                         

                 
                    conn.execute(text("drop table balancing_authority_temp;"))
                    conn.execute(text("drop table ba_adjusted_values_temp;")) 
                    conn.execute(text("drop table ba_emission_rate_temp;"))
                    trans.commit() 



                print('Success inserting balancing authority data.')  
                
 
                
            except Exception as e:
                print('Error inserting balancing authority data.', e)
                return {"error": str(e)}  

      
            #     BaFuelTypeGeneration.objects.update_or_create(
            #         bacode=BalancingAuthority.objects.get(bacode=item.get('bacode')),
            #         defaults={
            #             'bagenacl':sanitize_numeric(item.get('bagenacl')),
            #             'bagenaol':sanitize_numeric(item.get('bagenaol')),
            #             'bagenags':sanitize_numeric(item.get('bagenags')),
            #             'bagenanc':sanitize_numeric(item.get('bagenanc')),
            #             'bagenahy':sanitize_numeric(item.get('bagenahy')),
            #             'bagenabm':sanitize_numeric(item.get('bagenabm')),
            #             'bagenawi':sanitize_numeric(item.get('bagenawi')),
            #             'bagenaso':sanitize_numeric(item.get('bagenaso')),
            #             'bagenagt':sanitize_numeric(item.get('bagenagt')),
            #             'bagenaof':sanitize_numeric(item.get('bagenaof')),
            #             'bagenaop':sanitize_numeric(item.get('bagenaop')),
            #             'bagenatn':sanitize_numeric(item.get('bagenatn')),
            #             'bagenatr':sanitize_numeric(item.get('bagenatr')),
            #             'bagenath':sanitize_numeric(item.get('bagenath')),
            #             'bagenacy':sanitize_numeric(item.get('bagenacy')),
            #             'bagenacn':sanitize_numeric(item.get('bagenacn')),
            #             'year':item.get('year')
            #         }
            #     )

            #     BaFuelTypeGeneration.objects.update_or_create(
            #         bacode=BalancingAuthority.objects.get(bacode=item.get('bacode')),
            #         defaults={
            #             'banbnox':sanitize_numeric(item.get('banbnox')),
            #             'banbnxo':sanitize_numeric(item.get('banbnxo')),
            #             'banbso2':sanitize_numeric(item.get('banbso2')),
            #             'banbco2':sanitize_numeric(item.get('banbco2')),
            #             'banbch4':sanitize_numeric(item.get('banbch4')),
            #             'banbn2o':sanitize_numeric(item.get('banbn2o')),
            #             'banbc2e':sanitize_numeric(item.get('banbc2e')),
            #             'banbhg':sanitize_numeric(item.get('banbhg')),
            #             'banbgncl':sanitize_numeric(item.get('banbgncl')),
            #             'banbgnol':sanitize_numeric(item.get('banbgnol')),
            #             'banbgngs':sanitize_numeric(item.get('banbgngs')),
            #             'banbgnnc':sanitize_numeric(item.get('banbgnnc')),
            #             'banbgnhy':sanitize_numeric(item.get('banbgnhy')),
            #             'banbgnbm':sanitize_numeric(item.get('banbgnbm')),
            #             'banbgnwi':sanitize_numeric(item.get('banbgnwi')),
            #             'banbgnso':sanitize_numeric(item.get('banbgnso')),
            #             'banbgngt':sanitize_numeric(item.get('banbgngt')),
            #             'banbgnof':sanitize_numeric(item.get('banbgnof')),
            #             'banbgnop':sanitize_numeric(item.get('banbgnop')),
            #             'banbclpr':sanitize_numeric(item.get('banbclpr')),
            #             'banbolpr':sanitize_numeric(item.get('banbolpr')),
            #             'banbgspr':sanitize_numeric(item.get('banbgspr')),
            #             'banbncpr':sanitize_numeric(item.get('banbncpr')),
            #             'banbhypr':sanitize_numeric(item.get('banbhypr')),
            #             'banbbmpr':sanitize_numeric(item.get('banbbmpr')),
            #             'banbwipr':sanitize_numeric(item.get('banbwipr')),
            #             'banbsopr':sanitize_numeric(item.get('banbsopr')),
            #             'banbgtpr':sanitize_numeric(item.get('banbgtpr')),
            #             'banbofpr':sanitize_numeric(item.get('banbofpr')),
            #             'banboppr':sanitize_numeric(item.get('banboppr')),
            #             'year':item.get('year')
            #         }
            #     )

            #     BaNonBaseloadEmissionRate.objects.update_or_create(
            #         bacode=BalancingAuthority.objects.get(bacode=item.get('bacode')),
            #         defaults={
            #         'banbnox':sanitize_numeric(item.get('banbnox')),
            #         'banbnxo':sanitize_numeric(item.get('banbnxo')),
            #         'banbso2':sanitize_numeric(item.get('banbso2')),
            #         'banbco2':sanitize_numeric(item.get('banbco2')),
            #         'banbch4':sanitize_numeric(item.get('banbch4')),
            #         'banbn2o':sanitize_numeric(item.get('banbn2o')),
            #         'banbc2e':sanitize_numeric(item.get('banbc2e')),
            #         'banbhg':sanitize_numeric(item.get('banbhg')),
            #         'banbgncl':sanitize_numeric(item.get('banbgncl')),
            #         'banbgnol':sanitize_numeric(item.get('banbgnol')),
            #         'banbgngs':sanitize_numeric(item.get('banbgngs')),
            #         'banbgnnc':sanitize_numeric(item.get('banbgnnc')),
            #         'banbgnhy':sanitize_numeric(item.get('banbgnhy')),
            #         'banbgnbm':sanitize_numeric(item.get('banbgnbm')),
            #         'banbgnwi':sanitize_numeric(item.get('banbgnwi')),
            #         'banbgnso':sanitize_numeric(item.get('banbgnso')),
            #         'banbgngt':sanitize_numeric(item.get('banbgngt')),
            #         'banbgnof':sanitize_numeric(item.get('banbgnof')),
            #         'banbgnop':sanitize_numeric(item.get('banbgnop')),
            #         'banbclpr':sanitize_numeric(item.get('banbclpr')),
            #         'banbolpr':sanitize_numeric(item.get('banbolpr')),
            #         'banbgspr':sanitize_numeric(item.get('banbgspr')),
            #         'banbncpr':sanitize_numeric(item.get('banbncpr')),
            #         'banbhypr':sanitize_numeric(item.get('banbhypr')),
            #         'banbbmpr':sanitize_numeric(item.get('banbbmpr')),
            #         'banbwipr':sanitize_numeric(item.get('banbwipr')),
            #         'banbsopr':sanitize_numeric(item.get('banbsopr')),
            #         'banbgtpr':sanitize_numeric(item.get('banbgtpr')),
            #         'banbofpr':sanitize_numeric(item.get('banbofpr')),
            #         'banboppr':sanitize_numeric(item.get('banboppr')),
            #         'year':item.get('year')
            #         }
            #     )

            #     BaResourceMix.objects.update_or_create(
            #         bacode=BalancingAuthority.objects.get(bacode=item.get('bacode')),
            #         defaults={
            #             'baclpr':sanitize_numeric(item.get('baclpr')),
            #             'baolpr':sanitize_numeric(item.get('baolpr')),
            #             'bagspr':sanitize_numeric(item.get('bagspr')),
            #             'bancpr':sanitize_numeric(item.get('bancpr')),
            #             'bahypr':sanitize_numeric(item.get('bahypr')),
            #             'babmpr':sanitize_numeric(item.get('babmpr')),
            #             'bawipr':sanitize_numeric(item.get('bawipr')),
            #             'basopr':sanitize_numeric(item.get('basopr')),
            #             'bagtpr':sanitize_numeric(item.get('bagtpr')),
            #             'baofpr':sanitize_numeric(item.get('baofpr')),
            #             'baoppr':sanitize_numeric(item.get('baoppr')),
            #             'batnpr':sanitize_numeric(item.get('batnpr')),
            #             'batrpr':sanitize_numeric(item.get('batrpr')),
            #             'bathpr':sanitize_numeric(item.get('bathpr')),
            #             'bacypr':sanitize_numeric(item.get('bacypr')),
            #             'bacnpr':sanitize_numeric(item.get('bacnpr')),
            #             'year':item.get('year')
            #         }
            #     )

            return {"success": True, "message": "Data successfully inserted into the Balancing Auth table."}
        else:
            return {"error": f"Failed to connect to R API with status code {response.status_code}"}
    
    except Exception as e:
        return {"error": str(e)}