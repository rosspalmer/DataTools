
def class_data(df):

    df['class'] = df.apply(class_row, axis=1)
    return df

def class_row(row):

    clas_dic = class_dict('core')

    for clas in clas_dic.keys():
        if row.loc[clas_dic[clas]].sum() > 0:
            return clas

    return 'no_class'

def class_dict(mode='full'):

    dic = {}

    if mode == 'full':
        dic['class_203'] = ['feature_203','feature_82','feature_71','feature_193',
                            'feature_80','feature_201','feature_134','feature_219',
                            'feature_196']
    elif mode == 'core':
        dic['class_203'] = ['feature_203','feature_82','feature_71','feature_193',
                            'feature_80','feature_201','feature_196']

    if mode == 'full':
        dic['class_170'] = ['feature_170','feature_68','feature_54','feature_209',
                            'feature_179','feature_273','feature_155','feature_87',
                            'feature_223','feature_306','feature_134','feature_219',
                            'feature_86','feature_197','feature_345','feature_222']
    elif mode == 'core':
        dic['class_170'] = ['feature_170','feature_209','feature_179','feature_273',
                            'feature_155','feature_87','feature_223','feature_306',
                            'feature_86','feature_197','feature_345','feature_222']

    if mode == 'full':
        dic['class_232'] = ['feature_232','feature_313','feature_312','feature_307',
                            'feature_227','feature_315','feature_314','feature_134',
                            'feature_219','feature_301','feature_235','feature_233',
                            'feature_228','feature_160']
    elif mode == 'core':
        dic['class_232'] = ['feature_232','feature_313','feature_312','feature_307',
                            'feature_227','feature_315','feature_314','feature_301',
                            'feature_235','feature_233','feature_228','feature_160']

    if mode == 'full':
        dic['class_202'] = ['feature_54','feature_202','feature_171','feature_55',
                            'feature_81','feature_134','feature_219','feature_70',
                            'feature_154','feature_205','feature_156']
    elif mode == 'core':
        dic['class_202'] = ['feature_202','feature_171','feature_55','feature_81',
                            'feature_70','feature_154','feature_205','feature_156']

    if mode == 'full':
        dic['class_283'] = ['feature_283','feature_375','feature_291','feature_368',
                            'feature_290']
    elif mode == 'core':
        dic['class_283'] = ['feature_283','feature_375','feature_291','feature_368',
                            'feature_290']

    if mode == 'full':
        dic['class_73'] = ['feature_73']
    elif mode == 'core':
        dic['class_73'] = ['feature_73']

    return dic