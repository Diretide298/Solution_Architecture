import openpyxl, collections, json, re, csv

VOCAB = {
 'catalogue': ['ticket type','product','open-dated','dated ticket','time-slot','event management','resource','capacity','season pass','product lifecycle','catalogue','annual pass'],
 'orders':    ['order','booking','cart','checkout','reservation','refund','exchange','call center','call centre','b2b','reseller','front gate','upgrade','waiver'],
 'access':    ['access control','turnstile','gate','scan','entry','admission','validation','barrier','anti-passback','re-entry','credential read'],
 'promotions':['promotion','bundle','discount','voucher','coupon','offer','upsell','cross-sell','package deal','campaign code'],
 'finance':   ['revenue recognition','deferred revenue','ledger','journal','chart of accounts','accounting','tax','vat','settlement','reconcil','cash handling','shift variance','float','payment method','invoice','receipt'],
 'retail':    ['retail','sku','merchandise','stock item','barcode scan','retail pos'],
 'fnb':       ['menu','modifier','kitchen','kds','table','course','recipe','f&b','beverage','dining','order pad'],
 'reporting': ['report','dashboard','analytic','bi ','export','scheduled report','kpi','drill','self-service report'],
 'ai':        ['forecast','machine learning','model train','recommendation engine','dynamic pricing','fraud detection','llm','prompt','ai '],
 'identity':  ['user account','role','permission','rights','login','password','sso','authentication','audit log','event logging','access rights','user group'],
 'inventory': ['inventory','warehouse','procurement','purchase order','stock level','reorder','supplier','goods receipt'],
 'seating':   ['seat','seat map','row','section map','block','allocation'],
 'marketing-crm':['crm','loyalty','tier','points','segment','newsletter','email marketing','survey','review','case management','sla','consent','journey'],
 'queue':     ['queue','virtual queue','wait time','return time','ride reservation'],
 'white-label':['white-label','branding','theme','logo','app store','mobile app','deep link'],
 'subscription':['subscription','licence','license','tenant onboarding','quota','module marketplace'],
 'maintenance':['maintenance','work order','asset','inspection','safety','incident','spare part','preventive'],
 'workforce': ['employee app','shift roster','attendance','staff task','technician'],
 'assets':    ['digital asset','media library','image asset'],
 'games':     ['game','ride','arcade','redemption','prize'],
 'approvals': ['approval','approver','escalation','multi-level','authorisation chain','sign-off'],
}
DOMAIN_TO_CONTRACT = {
 'Ticketing Catalogue':'catalogue','Ticketing Sales':'orders','Admission and Access':'access',
 'Bundles and Promotions':'promotions','F&B & Guest Management':'finance','Payment':'finance',
 'Retail POS':'retail','F&B POS':'fnb','Unified Operations Dashboard':'reporting',
 'Games & F&B Integration':'games','Approval Workflows & Governance':'approvals',
 'Accreditation & Credential Management':'identity','Developer & API Management':'identity',
 'Inventory Management':'inventory','Device Management':'identity',
 'Maintenance & Safety Management':'maintenance','Employee Mobile App & AI Assistant':'workforce',
 'Guest Mobile App & Branding':'white-label','Subscription & Licensing Management':'subscription',
 'Seat Management & Venue Mapping':'seating','Marketing & CRM':'marketing-crm',
 'Digital Asset Management':'assets',
}

wb = openpyxl.load_workbook('sources/requirements/Ticvai_matrix_20260621_2.xlsx', data_only=True)
ws = wb['Funactionality ']
rows=[]
for i,r in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
    if all(c is None or str(c).strip()=='' for c in r): continue
    rows.append((i,[('' if c is None else str(c).strip()) for c in r]))
last=['','','','']
norm=[]
for n,r in rows:
    for k in range(4):
        if r[k]=='': r[k]=last[k]
        else: last[k]=r[k]
    norm.append((n,r))

sec=collections.OrderedDict()
for n,r in norm:
    k=(r[0],r[1],r[2],r[3])
    sec.setdefault(k,{'rows':0,'first':n,'last':n,'text':[]})
    sec[k]['rows']+=1; sec[k]['last']=n
    sec[k]['text'].append((r[5]+' '+(r[6] if len(r)>6 else '')).lower())

out=[]
for (did,dn,sid,sn),v in sec.items():
    blob=' '.join(v['text'])
    scores={c:sum(blob.count(t) for t in terms) for c,terms in VOCAB.items()}
    norm_scores={c:s/max(1,v['rows']) for c,s in scores.items()}
    top=sorted(norm_scores.items(), key=lambda x:-x[1])[:3]
    labelled=DOMAIN_TO_CONTRACT.get(dn,'?')
    mismatch = top[0][0]!=labelled and top[0][1]>0.5 and top[0][1] > norm_scores.get(labelled,0)*1.8
    out.append({'domain_id':did,'domain':dn,'sub_id':sid,'sub':sn,'rows':v['rows'],
        'first':v['first'],'last':v['last'],'labelled_contract':labelled,
        'signal_1':f'{top[0][0]}:{top[0][1]:.1f}','signal_2':f'{top[1][0]}:{top[1][1]:.1f}',
        'signal_3':f'{top[2][0]}:{top[2][1]:.1f}','mismatch':'YES' if mismatch else ''})

with open('/mnt/user-data/outputs/TICVAI_domain_drift_scan.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)

flag=[o for o in out if o['mismatch']]
print(f'sections={len(out)}  flagged={len(flag)}  rows_flagged={sum(o["rows"] for o in flag)}')
print()
by=collections.Counter()
for o in sorted(flag,key=lambda x:-x['rows']):
    print(f"  {o['sub_id']:<6}{o['sub'][:34]:<34} r={o['rows']:<4} labelled={o['labelled_contract']:<14} signal={o['signal_1']:<18} ({o['first']}-{o['last']})")
    by[(o['labelled_contract'],o['signal_1'].split(':')[0])]+=o['rows']
print()
print('=== net movement (rows) ===')
for (a,b),n in by.most_common():
    print(f'  {a:<14} -> {b:<14} {n}')
