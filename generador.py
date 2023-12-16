Ncampos=int(input('Numero de campos: '))
print()
camposBd=[]
campos=[]
tipos=[]
ltipos=[]
ntabla=input('Nombre de la tabla: ')
for i in range(Ncampos):
    camposBd.append(input('Nombre del campo de la BD: '))
print()
print('Varchar = 0 - Int = 1 - Date = 2 - Time = 3 - Bit = 4')
for i in range(Ncampos):
    tipos.append(input('Tipo de dato: '))
    if tipos[i]=='0':
        ltipos.append('VARHAR(255)')
    elif tipos[i]=='1':
        ltipos.append('INT')
    elif tipos[i]=='2':
        ltipos.append('DATE')
    elif tipos[i]=='3':
        ltipos.append('TIME')
    else:
        ltipos.append('BIT')
print()
npi=input('Nombre del procedimiento para insertar: ')
npe=input('Nombre del procedimiento para editar: ')
npd=input('Nombre del procedimiento para eliminar: ')
print()
print('INSERTAR')
print('CREATE PROCEDURE',npi,'(',end='')
for i in range(Ncampos):
    print('IN p_'+camposBd[i]+' '+ltipos[i],end=' ')
    if i<=Ncampos-2:
        print(',')
        print('\t',end='')
print(')\nBEGIN\n\tINSERT INTO',ntabla,'VALUES(',end='')
for i in range(Ncampos):
    print('p_'+camposBd[i],end=' ')
    if i<=Ncampos-2:
        print(',')
        print('\t',end='')
print(');\nEND;')
print()
print('EDITAR')
print('CREATE PROCEDURE',npe,'(',end='')
for i in range(Ncampos):
    print('IN p_'+camposBd[i]+' '+ltipos[i],end=' ')
    if i<=Ncampos-2:
        print(',')
        print('\t',end='')
print(')\nBEGIN\n\tUPDATE',ntabla,'SET ',end='')
for i in range(Ncampos):
    print(camposBd[i],'=','p_'+camposBd[i],end=' ')
    if i<=Ncampos-2:
        print(',')
        print('\t',end='')
print()
print('\tWHERE',camposBd[0],'= p_'+camposBd[0],';\nEND;')
print()
print('ELIMINAR')
print('CREATE PROCEDURE',npd,'(IN p_'+camposBd[0]+' '+ltipos[0]+')')
print('BEGIN\n\tDELETE FROM',ntabla,'WHERE',camposBd[0],'= p_'+camposBd[0],';\nEND;')
print()
for i in range(Ncampos):
    campos.append(camposBd[i].lower())
print()
print('JSON\n{')
for i in range(Ncampos):
    if tipos[i]=='1' or tipos[i]=='4':
        print(' '+'"'+campos[i]+'": ',end='')
    else:
        print(' '+'"'+campos[i]+'": ""',end='')
    if i<=Ncampos-2:
        print(',')
print()
print('}')
print()
print()
#print('Get = 0 - Post = 1 - Put = 2 - Delete = 3')
print('Get')
print('''app.get('/get'''+ntabla.capitalize()+'''', (req, res) => {
    connection.query('', (err, results) => {
        if (err) {
            console.error('error: ',err);
            res.status(500).json({err});
            return;
        }
        res.json(results);
    });
});''')
print()
print()
print('Post')
print('''app.post('/post'''+ntabla.capitalize()+'''',(req,res)=>{
    const{''')
for i in range(Ncampos):
    print('\t\t'+campos[i],end='')
    if i<=Ncampos-2:
        print(',')
print('''
    }=req.body;
    connection.query('CALL''',npi+'''(''',end='')
for i in range(Ncampos):
    print('?',end='')
    if i<=Ncampos-2:
        print(',',end='')
print(''')', [ ''')
for i in range(Ncampos):
    print('\t'+campos[i],end='')
    if i<=Ncampos-2:
        print(',')
print('''],(err,results)=>{
            if(err){
                console.error('error: ',err);
                res.status(500).json({err});
                return;
            }
            res.json({results});    
        }
    );
});''')
print()
print()
print('Put')
print('''app.put('/put'''+ntabla.capitalize()+'''/:'''+campos[0]+'''',(req,res)=>{
    const{''',campos[0],'''}=req.params;
    const{''')
for i in range(Ncampos-1):
    print('\t\t'+campos[i+1],end='')
    if i<=Ncampos-3:
        print(',')
print('''
    }=req.body;
    connection.query('CALL''',npe+'''(''',end='')
for i in range(Ncampos):
    print('?',end='')
    if i<=Ncampos-2:
        print(',',end='')
print(''')', [ ''')
for i in range(Ncampos):
    print('\t'+campos[i],end='')
    if i<=Ncampos-2:
        print(',')
print('''],(err,results)=>{
            if(err){
                console.error('error: ',err);
                res.status(500).json({err});
                return;
            }
            res.json({results});    
        }
    );
});''')
print()
print()
print('Delete')
print('''app.delete('/del'''+ntabla.capitalize()+'''/:'''+campos[0]+'''',(req,res)=>{
    const{''',campos[0],'''}=req.params;
    connection.query('CALL''',npd+'''(?)',[''',campos[0],'''],(err,results)=>{
        if(err){
            console.error('error: ',err);
            res.status(500).json({err});
            return;
        }
        res.json({results});    
    });
});''')