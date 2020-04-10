SELECT r.id,
                r.rresvsaleid,
                r.sequence,
                r.taxfeecode,
                r.postaxfeeamount,
                r.initialbookingdate,
                r.generationdate
            FROM DLEX_GSREPORT.rresv_sale_taxfees r 
            WHERE generationdate >= TO_DATE('2020-04-07 00:00:00', 'yyyy-MM-dd hh24:mi:ss')
            AND generationdate < TO_DATE('2020-04-08 00:00:00', 'yyyy-MM-dd hh24:mi:ss')
            SELECT r.id,
                r.rresvsaleid,
                r.sequence,
                r.primarydocnumber,
                r.issueddate,
                r.initialbookingdate, 
                r.generationdate
            FROM DLEX_GSREPORT.rresv_sale_document r 
            WHERE generationdate >= TO_DATE('2020-04-06 00:00:00', 'yyyy-MM-dd hh24:mi:ss')
            AND generationdate < TO_DATE('2020-04-07 00:00:00', 'yyyy-MM-dd hh24:mi:ss')