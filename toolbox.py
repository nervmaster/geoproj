#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import csv
import cv2
import operator
import numpy as np
from imgaug import augmenters as iaa
from random import randint
from sklearn import preprocessing
from multiprocessing import Process, Lock, Queue, Pool, Manager
from skimage.feature import greycomatrix, greycoprops
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import LabColor
import scipy.stats as st
from testopencs import crop_new_image
import math
import gc


def crop_geo_set(folder_names):
    # For each folder
    for f in folder_names:
        path = './' + f + '/'
        subfolders = os.listdir(f)

        for subf in subfolders:
            subpath = path + '/' + subf + '/'

            files = os.listdir(subpath)
            imlist = list()

            # Coletando arquivos das pastas
            for arq in files:
                imlist.append(cv2.imread(subpath + arq))

            # Cortando as imagens da pasta
            xpl, ppl = crop_new_image(imlist)

            # Escrever as imagens cortadas em uma nova pasta de teste
            impath = './train/' + f + '/' + subf + '/'
            try:
                os.mkdir('./train/')
            except:
                print 'train folder already created'
            try:
                os.mkdir('./train/' + f + '/')
            except:
                print 'train ' + f + ' already created'
            try:
                os.mkdir('./train/' + f + '/' + subf + '/')
            except:
                print 'subfolder already created'
            for i in range(len(xpl)):
                cv2.imwrite(impath + 'x' + str(i) + '.png', xpl[i])
            for i in range(len(ppl)):
                cv2.imwrite(impath + 'p' + str(i) + '.png', ppl[i])


def make_csv(filepath):
    try:
        arq = open(filepath, 'w')
    except Exception as e:
        print "Nao foi possivel abrir o arquivo", e
        exit(1)
    print 'esrevendo header'
    writer = csv.writer(arq, delimiter=';')
    header = list()
    header.append('label')
    header.extend(('xpl_l', 'xpl_a', 'xpl_b'))
    header.extend(('ppl_l', 'ppl_a', 'ppl_b'))
    header.append('biref')
    header.append('pleoc')
    header.extend(('tex_1', 'tex_2', 'tex_3', 'tex_4'))
    header.extend(('opa_l_xpl', 'opa_l_ppl',
                   'opa_stddev_xpl', 'opa_stddev_ppl'))
    writer.writerow(header)
    arq.flush()
    return arq, writer


def conf_interval_dict(sample):
    result = dict()
    conf = 0.95
    result['xpl_l'] = st.norm.interval(conf, loc=np.mean(
        sample[:, 0:1]), scale=np.std(sample[:, 0:1]))
    result['xpl_a'] = st.norm.interval(conf, loc=np.mean(
        sample[:, 1:2]), scale=np.std(sample[:, 1:2]))
    result['xpl_b'] = st.norm.interval(conf, loc=np.mean(
        sample[:, 2:3]), scale=np.std(sample[:, 2:3]))
    result['ppl_l'] = st.norm.interval(conf, loc=np.mean(
        sample[:, 3:4]), scale=np.std(sample[:, 3:4]))
    result['ppl_a'] = st.norm.interval(conf, loc=np.mean(
        sample[:, 4:5]), scale=np.std(sample[:, 4:5]))
    result['ppl_b'] = st.norm.interval(conf, loc=np.mean(
        sample[:, 5:6]), scale=np.std(sample[:, 5:6]))
    result['biref_l'] = st.norm.interval(conf, loc=np.mean(
        sample[:, 6:7]), scale=np.std(sample[:, 6:7]))
    result['biref_a'] = st.norm.interval(conf, loc=np.mean(
        sample[:, 7:8]), scale=np.std(sample[:, 7:8]))
    result['biref_b'] = st.norm.interval(conf, loc=np.mean(
        sample[:, 8:9]), scale=np.std(sample[:, 8:9]))
    result['pleoc_l'] = st.norm.interval(conf, loc=np.mean(
        sample[:, 9:10]), scale=np.std(sample[:, 9:10]))
    result['pleoc_a'] = st.norm.interval(conf, loc=np.mean(
        sample[:, 10:11]), scale=np.std(sample[:, 10:11]))
    result['pleoc_b'] = st.norm.interval(conf, loc=np.mean(
        sample[:, 11:12]), scale=np.std(sample[:, 11:12]))
    result['tex_1'] = st.norm.interval(conf, loc=np.mean(
        sample[:, 13:14]), scale=np.std(sample[:, 13:14]))
    result['tex_2'] = st.norm.interval(conf, loc=np.mean(
        sample[:, 14:15]), scale=np.std(sample[:, 14:15]))
    result['tex_3'] = st.norm.interval(conf, loc=np.mean(
        sample[:, 15:16]), scale=np.std(sample[:, 15:16]))
    result['opa_1'] = st.norm.interval(conf, loc=np.mean(
        sample[:, 16:17]), scale=np.std(sample[:, 16:17]))
    return result


def make_confidence_interval(data, labels):
    result = dict()
    current = labels[0]
    sample = list()
    for i in range(0, len(labels)):
        if(current == labels[i]):
            sample.append(data[i])
        else:
            sample = np.asarray(sample)
            if(len(sample) > 1):
                result[current] = conf_interval_dict(sample)
            else:
                pass
            current = labels[i]
            sample = list()
    result[current] = dict()
    sample = np.asarray(sample)
    result[current] = conf_interval_dict(sample)
    return result

# Criando uma array das labels


def get_aligholi_number_label(pos):
    if pos <= 5:
        return 0
    if pos <= 11:
        return 1
    if pos <= 17:
        return 2
    if pos <= 31:
        return 3
    if pos <= 34:
        return 4
    if pos <= 39:
        return 5
    if pos <= 44:
        return 6
    if pos <= 54:
        return 7
    if pos <= 57:
        return 8
    if pos <= 59:
        return 9
    if pos <= 60:
        return 10
    if pos <= 67:
        return 11
    if pos <= 71:
        return 12
    if pos <= 76:
        return 13
    if pos <= 77:
        return 14
    if pos <= 79:
        return 15
    if pos <= 81:
        return 16
    else:
        return 17


def get_aligholi_training_label(pos, numbers=False):
    if pos <= 5:
        return 'Anthophilite'
    if pos <= 11:
        return 'Augite'
    if pos <= 17:
        return 'Olivine'
    if pos <= 31:
        return 'Biotite'
    if pos <= 34:
        return 'Muscovite'
    if pos <= 39:
        return 'Calcite'
    if pos <= 44:
        return 'Brown hornblende'
    if pos <= 54:
        return 'Green hornblende'
    if pos <= 57:
        return 'Chlorite'
    if pos <= 59:
        return 'Opx'
    if pos <= 60:
        return 'Apatite'
    if pos <= 67:
        return 'Quartz'
    if pos <= 71:
        return 'PLagioclase'
    if pos <= 76:
        return 'Orthoclase'
    if pos <= 77:
        return 'Microcline'
    if pos <= 79:
        return 'Sanidine'
    if pos <= 81:
        return 'lucite'
    else:
        return 'Garnet'

# dentro de um diretorio
# iterar os arquivos XPL
# fazer media geral xpl


def make_avg_color(im_list, light_type):
    bob = list()
    for im in im_list:
        im_lab = to_float_lab(im)
        im_lab = extract_info(np.average, im_lab)
        bob.append(im_lab)
    return merge_array(np.average, bob)


def make_pleochroism_color(im_list, light_type):
    images = list()
    min_l = [200] * 3
    max_l = [0] * 3
    for im in im_list:
        im_lab = to_float_lab(im)
        im_lab = extract_info(np.average, im)
        if(im_lab[0] < min_l[0]):
            min_l = im_lab
        if(im_lab[0] > max_l[0]):
            max_l = im_lab
    a = LabColor(lab_l=max_l[0], lab_a=max_l[1], lab_b=max_l[2])
    b = LabColor(lab_l=min_l[0], lab_a=min_l[1], lab_b=min_l[2])
    return np.asarray(delta_e_cie2000(a, b))


def select_training_sets(collection, labels, targets):
    result = dict()
    result['new_entry_set'] = list()
    result['new_entry_labels'] = list()

    for target in targets:
        result['new_entry_set'].append(collection[target])
        result['new_entry_labels'].append(labels[target])
    result['labels'] = np.delete(labels, targets, 0)
    result['training'] = np.delete(collection, targets, 0)
    result['new_entry_set'] = np.asarray(result['new_entry_set'])
    result['new_entry_labels'] = np.asarray(result['new_entry_labels'])
    return result


def make_training_sets(collection, labels):
    size = len(collection) / 10
    result = dict()
    result['new_entry_set'] = list()
    result['new_entry_labels'] = list()
    n_pick = 0
    while n_pick < size:
        target = randint(0, len(collection) - 1)
        if (target > 0 and labels[target] == labels[target - 1]) or (target < len(collection) - 1 and labels[target] == labels[target + 1]):
            result['new_entry_set'].append(collection[target])
            result['new_entry_labels'].append(labels[target])
            collection = np.delete(collection, target, 0)
            labels = np.delete(labels, target, 0)
            n_pick += 1
    result['labels'] = labels
    result['training'] = collection
    result['new_entry_set'] = np.asarray(result['new_entry_set'])
    result['new_entry_labels'] = np.asarray(result['new_entry_labels'])
    return result


def make_texture_param(im_list):
    bob = list()
    for im in im_list:
        bob.append(texture_param(im))
    result = np.zeros((len(bob), 4), dtype=np.float32)
    for i in range(len(bob[0])):
        for j in range(len(bob)):
            result[j][i] = bob[j][i]
    return np.average(result, axis=0)


def extinction_class(im_list):
    images = list()
    for im in im_list:
        images.append(to_float_lab(im))

    pos = get_extinction_pos(images)
    pos = pos * 5
    ext = -1
    if(0 <= pos <= 5 or 85 <= pos <= 90):
        ext = 1
    elif(10 <= pos <= 20 or 70 <= pos <= 80):
        ext = 2
    elif(25 <= pos <= 35 or 55 <= pos <= 65):
        ext = 3
    else:
        ext = 4

    return ext


def make_opacity_param(im_ppl, im_xpl):
    images = list()
    for im in im_ppl:
        images.append(to_float_lab(im))
    result = opacity_param(images)

    images = list()
    for im in im_xpl:
        images.append(to_float_lab(im))
    return np.append(result, opacity_param(images))


def get_mineral_name_number(str):
    if "Biotita" in str:
        return 3
    elif "Quartzo" in str:
        return 11
    elif "Ortoclasio" in str:
        return 13


def iterate_gathered_data(arq, writer, param, pairs=1):
    base_path = './Teste/'

    root = os.listdir(base_path)

    for mineral in root:
        print mineral

        xpl = list()
        ppl = list()
        all_set = list()
        labels = list()

        mineralpath = base_path + mineral + '/'

        photos_folders = os.listdir(mineralpath)

        for folder in photos_folders:
            photopath = mineralpath + folder + '/'

            photos = os.listdir(photopath)

            if "NP" in folder:
                lista = ppl
            else:
                lista = xpl

            for i in photos[:40]:
                lista.append(cv2.imread(photopath + i))

        # Coloca label e row
        label_number = get_mineral_name_number(mineral)
        for x in xpl:
            for p in ppl:
                all_set.append(extract_params_from_imset(param, [x], [p]))
                labels.append(label_number)

        for label, row in zip(labels, all_set):
            writer.writerow(np.append(label, row))
        arq.flush()
        del labels
        del xpl
        del ppl
        del all_set


def extract_params_from_imset(param, im_xpl, im_ppl, normalize=False):
    # desired number of pairs
    arg = np.empty([0, 0])
    if('xpl' in param):
        xpl = make_avg_color(im_xpl, 'x')
        arg = np.append(arg, xpl)
    if('ppl' in param):
        ppl = make_avg_color(im_ppl, 'p')
        arg = np.append(arg, ppl)
    if('biref' in param):
        biref = make_pleochroism_color(im_xpl, 'x')
        arg = np.append(arg, biref)
    if('pleoc' in param):
        pleoc = make_pleochroism_color(im_ppl, 'p')
        arg = np.append(arg, pleoc)
    if('tex' in param):
        tex = make_texture_param(im_xpl + im_ppl)
        arg = np.append(arg, tex)
    if('opa' in param):
        opa = make_opacity_param(im_ppl, im_xpl)
        arg = np.append(arg, opa)

    if(normalize):
        arg = preprocessing.normalize(arg[:, np.newaxis], axis=0).ravel()
    return arg


def parse_folder(folder, label, param, fila_data, fila_label):
    def st(aug): return iaa.Sometimes(0.95, aug)
    print folder
    #Get all images from HD
    for i in range(1, 20):
        print i, folder
        x = cv2.imread(folder + 'x' + str(i) + '.png')
        for j in range(1, 20):
                images.append(x)
                images.append(cv2.imread(folder + 'p' + str(j) + '.png'))
                labels.append(label)
    print 'done with hd files', folder
    #With list do the augmentations
    seq = iaa.Sequential([
            iaa.Crop(px=(0, 16)),
            iaa.Fliplr(0.95),
            iaa.Flipud(0.95),
            iaa.GaussianBlur(sigma=(0, 3.0)),
            st(iaa.Affine(
                scale=(0.8, 1.2),
                rotate=(-180, 180)
            ))],
            random_order=True
        )

    images = seq.augment_images(images)
    
    # extract param from img aug
    data = list()
    for i in xrange(0, len(images), 2):
        data.append(extract_params_from_imset(
            param, [images[i]], [images[i + 1]]))
    del images
    print 'putting data on queue', folder
    # put them all on the queue
    fila_data.put(data)
    fila_label.put(labels)
    # END

    print 'fim', folder
    


def iterate_alligholli_dataset(arq, writer, param):
    # Itera o dataset
    base_path = './MIfile/MI'
    
    print 'iniciando paralelismo'
    #iniciar o paralelismo
    pool = Pool(2)
    args = list()

    print 'iniciando filas'
    #iniciar as filas
    m = Manager()
    fila_data = m.Queue()
    fila_label = m.Queue()
    
    mpr = list()
    print 'iniciando processos'
    for i in range(1, 84):
        folder = base_path + str(i) + '/'
        label = get_aligholi_number_label(i)
        mpr.append(pool.apply_async(parse_folder, (folder, label, param, fila_data, fila_label)))
    pool.close()
    print 'rotina de escrita durante os processos'
    while True:
        try:
            [r.get(timeout = 1) for r in mpr]
            break
        except:
            rows = fila_data.get()
            labels = fila_label.get()
            for label, row in zip(labels, data):
                writer.writerow(np.append(label, row))
            arq.flush()
    print 'escrevendo os remanescentes'
    while not fila_label.empty():
        rows = fila_data.get()
        labels = fila_data.get()
        for label, row in zip(labels, rows):
            writer.writerow(np.append(label, row))

    arq.flush()

def read_from_csv(path, param):
    result = dict()
    result['entries'] = list()
    result['labels'] = list()

    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            result['labels'].append(row['label'])
            arg = list()
            if 'xpl' in param:
                arg.extend((row['xpl_l'], row['xpl_a'], row['xpl_b']))
            if 'ppl' in param:
                arg.extend((row['ppl_l'], row['ppl_a'], row['ppl_b']))
            if 'biref' in param:
                arg.append(row['biref'])
            if 'pleoc' in param:
                arg.append(row['pleoc'])
            if 'tex' in param:
                arg.extend((row['tex_1'], row['tex_2'],
                            row['tex_3'], row['tex_4']))
            if 'opa' in param:
                arg.extend((row['opa_l_xpl'], row['opa_l_ppl'],
                            row['opa_stddev_xpl'], row['opa_stddev_ppl']))
            result['entries'].append(arg)
        result['entries'] = np.asarray(result['entries']).astype(np.float)
        result['labels'] = np.asarray(result['labels']).astype(np.float)
        return result

# classifica o minerio de acordo com seu angulo de extincao


def get_extinction_pos(collection):
    menor_l = 9999
    pos = -1

    for i in range(len(collection)):
        l, _, _ = cv2.split(collection[i])

        l = np.average(l, axis=0)
        l = np.average(l, axis=0)

        if(l < menor_l):
            menor_l = l
            pos = i

    return pos

# pega o brilho e seu desvio padrao


def opacity_param(collection):
    for i in range(len(collection)):
        l, _, _ = cv2.split(collection[i])
        l = np.average(l, axis=0)
        l = np.average(l, axis=0)

        dev = cv2.meanStdDev(collection[i])
        dev = np.average(dev, axis=0)
        dev = dev[0]

        if(i == 0):
            all_l = l
            all_stddev = dev
        else:
            all_l = np.append(all_l, l)
            all_stddev = np.append(all_stddev, dev)

    l = all_l
    dev = all_stddev
    if(len(collection) > 1):
        l = np.average(all_l, axis=0)
        dev = np.average(all_stddev, axis=0)

    return np.append(l, dev)

# Função de calcular os parâmetros de Textura


def texture_param(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hist = greycomatrix(image, (1, 1), [0], 256, symmetric=False, normed=False)
    result = list()
    props = ['contrast', 'homogeneity', 'energy', 'ASM']
    for p in props:
        im_res = greycoprops(hist, p)
        try:
            result.append(math.log10(im_res[0]))
        except:
            result.append(0)
    return result

# Em uma imagem transforma em float e em LAB


def to_float_lab(image, normalize=False):
    image = np.float32(image)
    image = image / 255.0
    image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    if(normalize):
        image[:, :, 0] = image[:, :, 0] / 100.0
        image[:, :, 1] = (image[:, :, 1] + 127.0) / 254.0
        image[:, :, 2] = (image[:, :, 2] + 127.0) / 254.0

    return image

# Extrai as informacoes da imagem
# type -> o tipo de informação a ser extraída
#		- 'avg'
#		- 'min'
#		- 'max'
# func -> funcao np para extrair a informacao
#		- np.average
#		- np.min
#		- np.max
# image -> imagem ou ROI que vai ser extraido


def extract_info(func, image):
    image = func(image, axis=0)
    image = func(image, axis=0)
    return image

# func -> funcao np para extrair a informacao
#		- np.average
#		- np.min
#		- np.max
# collection -> colecao de informacoes da imagem


def merge_array(func, collection):
    arr = np.asarray(collection)
    return func(arr, axis=0)
