# -*- coding: utf-8 -*-
#GerarRelatorio.py
"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFolderDestination,
                       QgsProcessingParameterField,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink)
import os, pdfkit
from qgis.PyQt.QtGui import QIcon

class GerarRelatorio(QgsProcessingAlgorithm):

    def tr(self, string):

        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return GerarRelatorio()

    def name(self):

        return 'gerarrelatorio'

    def displayName(self):

        return self.tr('Gerar Relatório')

    def group(self):

        return self.tr('TPF')

    def groupId(self):

        return 'TPF'
    
    def icon(self):
        return QIcon(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images/document.png'))
    
    def shortHelpString(self):

        return self.tr(''' Esta Ferramenta gera vários relatórios a partir de uma <b>camada de pontos</b>.
        É importante definir o <b>campo</b> que vai nomear os arquivos, sendo este chave primária''')

    CAMADA = 'CAMADA'
    PASTA = 'PASTA'
    CAMPO = 'CAMPO'
    PDF = 'PDF'

    def initAlgorithm(self, config=None):

        #INPUT
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.CAMADA,
                self.tr('Camada de Entrada'),
                [QgsProcessing.TypeVectorPoint] #QgsProcessing.TypeVectorLine
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.CAMPO,
                self.tr('Campo para nomear arquivo'),
                parentLayerParameterName = self.CAMADA
            )
        )


        #OUTPUT
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.PASTA,
                self.tr('Pasta para salvar os relatórios'),
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.PDF,
                self.tr('Exportar como PDF'),
            )
        )



    def processAlgorithm(self, parameters, context, feedback):

        camada = self.parameterAsSource(
            parameters,
            self.CAMADA,
            context
        )




        if camada is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.CAMADA))

        campo = self.parameterAsFields(
            parameters,
            self.CAMPO,
            context
        )

        pasta_saida = self.parameterAsString(
            parameters,
            self.PASTA,
            context
        )

        if 'Temp' in pasta_saida:
           raise QgsProcessingException('A pasta de entrada não pode ser temporária!')

        salvar_pdf = self.parameterAsBool(
            parameters,
            self.PDF,
            context
        )
        #Algoritmo
        texto_modelo = ''' <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
        <html>
        <head>
          <meta content="text/html; charset=ISO-8859-1"
         http-equiv="content-type">
          <title></title>
        </head>
        <body>
        <p class="MsoNormal" style="line-height: normal;"><b><span
         style="font-size: 24pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">RELAT&Oacute;RIO
        DE
        CADASTRO<o:p></o:p></span></b></p>
        <p class="MsoNormal" style="line-height: normal;"><b><span
         style="font-size: 18pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">RESUMO<o:p></o:p></span></b></p>
        <div class="MsoNormal"
         style="margin-bottom: 0cm; text-align: center; line-height: normal;"
         align="center"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">
        <hr style="color: black;" align="center"
         noshade="noshade" size="2" width="100%"></span></div>
        <table class="MsoNormalTable" style="" border="0"
         cellpadding="0">
          <tbody>
            <tr style="">
              <td
         style="padding: 0.75pt; background: rgb(36, 64, 97) none repeat scroll 0% 50%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: white;">NOME
        DO PROJETO</span><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
              </td>
              <td colspan="3"
         style="padding: 0.75pt; background: rgb(219, 229, 241) none repeat scroll 0% 50%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">Insira
        aqui o nome do projeto</span><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">DATA
        DE EMISS&Atilde;O<o:p></o:p></span></p>
              </td>
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">MUNIC&Iacute;PIO<o:p></o:p></span></p>
              </td>
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">BAIRRO<o:p></o:p></span></p>
              </td>
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">N&ordm;
        DE CADASTROS<o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">[DATA]<o:p></o:p></span></p>
              </td>
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">Recife
        (PE)<o:p></o:p></span></p>
              </td>
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">Imbiribeira<o:p></o:p></span></p>
              </td>
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">[n_cadastro]<o:p></o:p></span></p>
              </td>
            </tr>
          </tbody>
        </table>
        <p class="MsoNormal" style="line-height: normal;"><b><span
         style="font-size: 18pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">CADASTRO<o:p></o:p></span></b></p>
        <div class="MsoNormal"
         style="margin-bottom: 0cm; text-align: center; line-height: normal;"
         align="center"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">
        <hr style="color: black;" align="center"
         noshade="noshade" size="2" width="100%"></span></div>
        <table class="MsoNormalTable" style="width: 425pt;"
         border="0" cellpadding="0" width="567">
          <tbody>
            <tr style="">
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">ID
        DO LOTE<o:p></o:p></span></p>
              </td>
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">COORDENADAS
        UTM<o:p></o:p></span></p>
              </td>
              <td style="padding: 0.75pt; width: 214.65pt;"
         width="286">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; text-align: center; line-height: normal;"
         align="center"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">MAPA
        DO LOTE<o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td
         style="padding: 0.75pt; background: rgb(219, 229, 241) none repeat scroll 0% 50%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><b><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">[LOTE]</span></b><b><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></b></p>
              </td>
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">X:
        [X]<br>
        Y: [Y]<o:p></o:p></span></p>
              </td>
              <td rowspan="7"
         style="padding: 0.75pt; width: 214.65pt;" width="286"><img
         style="width: 400px; height: 250px;" alt="CROQUI"
         src="file:///[IMG2]"></td>
            </tr>
            <tr style="">
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">RUA<o:p></o:p></span></p>
              </td>
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">N&Uacute;MERO<o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">[RUA]<o:p></o:p></span></p>
              </td>
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">[IMOVEL]<o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td colspan="2" style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">NOME
        DO PROPRIET&Aacute;IRO<o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td colspan="2" style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">[PROPRIETARIO]<o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td colspan="2" style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">DATA
        E HORA DO LEVANTAMENTO<o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td colspan="2" style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">[DATA_HORA]<o:p></o:p></span></p>
              </td>
            </tr>
          </tbody>
        </table>
        <p class="MsoNormal" style="line-height: normal;"><b><span
         style="font-size: 18pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">IM&Oacute;VEL<o:p></o:p></span></b></p>
        <div class="MsoNormal"
         style="margin-bottom: 0cm; text-align: center; line-height: normal;"
         align="center"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">
        <hr style="color: black;" align="center"
         noshade="noshade" size="2" width="100%"></span></div>
        <table class="MsoNormalTable" style="width: 425pt;"
         border="0" cellpadding="0" width="567">
          <tbody>
            <tr style="">
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">USO
        DO IM&Oacute;VEL<o:p></o:p></span></p>
              </td>
              <td style="padding: 0.75pt; width: 294.65pt;"
         width="393">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; text-align: center; line-height: normal;"
         align="center"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">PADR&Atilde;O
        CONSTRUTIVO<o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">[USO_IMOVEL]<o:p></o:p></span></p>
              </td>
              <td style="padding: 0.75pt; width: 294.65pt;"
         width="393">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; text-align: center; line-height: normal;"
         align="center"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">[P_CONS]<o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">&Aacute;REA
        DO LOTE (m&sup2;)<o:p></o:p></span></p>
              </td>
              <td style="padding: 0.75pt; width: 294.65pt;"
         width="393">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; text-align: center; line-height: normal;"
         align="center"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">FOTO
        DO IM&Oacute;VEL<o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">[AREA]<o:p></o:p></span></p>
              </td>
              <td rowspan="11"
         style="padding: 0.75pt; width: 294.65pt;" width="393"><img
         style="height: 250px;" alt="FOTO"
         src="file:///[IMG]"></td>
            </tr>
            <tr style="">
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">LIGA&Ccedil;&Atilde;O
        DE &Aacute;GUA<o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">[AGUA]<o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">LIGA&Ccedil;&Atilde;O
        DE ESGOTO<o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">[ESGOTO]<o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">N&ordm;
        DE PAVIMENTOS<o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">[NPAV]<o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">N&ordm;
        DE MORADORES<o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">[N_MORADORES]<o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">OBSERVA&Ccedil;&Otilde;ES<o:p></o:p></span></p>
              </td>
            </tr>
            <tr style="">
              <td style="padding: 0.75pt;">
              <p class="MsoNormal"
         style="margin-bottom: 0cm; line-height: normal;"><span
         style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;">[OBS]<o:p></o:p></span></p>
              </td>
            </tr>
          </tbody>
        </table>
        <p class="MsoNormal"><o:p>&nbsp;</o:p></p>
        </body>
        </html>


        '''

        def str2HTML(texto):
            if texto:
                dicHTML = {'Á': '&Aacute;',	'á': '&aacute;',	'Â': '&Acirc;',	'â': '&acirc;',	'À': '&Agrave;',	'à': '&agrave;',	'Å': '&Aring;',	'å': '&aring;',	'Ã': '&Atilde;',	'ã': '&atilde;',	'Ä': '&Auml;',	'ä': '&auml;', 'ú': '&uacute;', 'Ú': '&Uacute;', 'Æ': '&AElig;',	'æ': '&aelig;',	'É': '&Eacute;',	'é': '&eacute;',	'Ê': '&Ecirc;',	'ê': '&ecirc;',	'È': '&Egrave;',	'è': '&egrave;',	'Ë': '&Euml;',	'ë': '&Euml;',	'Ð': '&ETH;',	'ð': '&eth;',	'Í': '&Iacute;',	'í': '&iacute;',	'Î': '&Icirc;',	'î': '&icirc;',	'Ì': '&Igrave;',	'ì': '&igrave;',	'Ï': '&Iuml;',	'ï': '&iuml;',	'Ó': '&Oacute;',	'ó': '&oacute;',	'Ô': '&Ocirc;',	'ô': '&ocirc;',	'Ò': '&Ograve;', 'Õ': '&Otilde;', 'õ': '&otilde;',	'ò': '&ograve;',	'Ø': '&Oslash;',	'ø': '&oslash;',	'Ù': '&Ugrave;',	'ù': '&ugrave;',	'Ü': '&Uuml;',	'ü': '&uuml;',	'Ç': '&Ccedil;',	'ç': '&ccedil;',	'Ñ': '&Ntilde;',	'ñ': '&ntilde;',	'Ý': '&Yacute;',	'ý': '&yacute;',	'"': '&quot;', '”': '&quot;',	'<': '&lt;',	'>': '&gt;',	'®️': '&reg;',	'©️': '&copy;',	'\'': '&apos;', 'ª': '&ordf;', 'º': '&ordm', '°':'&deg;'}
                for item in dicHTML:
                    if item in texto:
                        texto = texto.replace(item, dicHTML[item])
                return texto
            else:
                return ''


        #camada = iface.activeLayer()
        tam = camada.featureCount() #Quantidade de feições da camada
        total = 100.0 / tam if tam else 0

        for k, feat in enumerate(camada.getFeatures()):
            # Geometria
            texto = texto_modelo
            geom = feat.geometry()
            coord = geom.asPoint() # asPolygon() , asPolyline()
            X = coord.x()
            Y = coord.y()

            # Atributos
            #att = feat.attributes() # ler todos os atributos
            #n_pav = feat['n_pav'] # ler atributo específico

            # ID
            id = feat.id() # feat['fid']
            print (id, feat['fid'])
        #    print(X, Y)
        #    print(n_pav)

            uso_imovel = {1: 'HABITACIONAL',
                          2: 'COMERCIAL',
                          3: 'SERVIÇO PÚBLICO',
                          4: 'MISTO',
                          5: 'OUTRO',
                          }

            dic = { '[DATA]': feat['data'].toPyDateTime().strftime("%x"),
                   '[NPAV]': str(feat['n_pav']),
                   '[CONTADOR]': str(feat['fid']),
                   '[EDIFICACAO]': str(tam),
                   '[RUA]': feat['RUA'],
                   '[IMOVEL]': str(feat['n_Imovel']),
                   '[PROPRIETARIO]': feat['PROP'],
                   '[DATA_HORA]': feat['data'].toPyDateTime().strftime("%x"),
                   '[USO_IMOVEL]': uso_imovel[feat['USO_IMOVEL']]if feat['USO_IMOVEL'] in  uso_imovel else 'Não Preenchido',
                   '[AGUA]': str(feat['AGUA']),
                   '[ESGOTO]': str(feat['ESGOTO']),
                   '[N_MORADORES]': str(feat['n_Moradores']),
                   '[OBS]': str(feat['OBS']),
                   '[P_CONS]': str(feat['PADRAO_CONST']),
                   '[X]': '{0:,.2f}' .format(X),
                   '[Y]': '{0:,.2f}' .format(Y),
                   '[IMG]': feat['caminho2'],
                   '[IMG2]': feat['caminho'],

                   }

            #Onde ocorre a substituição
            for item in dic:
                texto = texto.replace(item, str2HTML(dic[item]))

            nome_arquivo = str(feat[campo[0]])
            #Gerar arquivo
            arq = open(os.path.join(pasta_saida, nome_arquivo + '.html'),'w')
            arq.write(texto)
            arq.close()

            if feedback.isCanceled():
                break

            feedback.setProgress(int((k+1) * total))

        '''
        # Send some information to the user
        feedback.pushInfo('CRS is {}'.format(source.sourceCrs().authid()))

        # If sink was not created, throw an exception to indicate that the algorithm
        # encountered a fatal error. The exception text can be any string, but in this
        # case we use the pre-built invalidSinkError method to return a standard
        # helper text for when a sink cannot be evaluated
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        # Compute the number of steps to display within the progress bar and
        # get features from source
        total = 100.0 / source.featureCount() if source.featureCount() else 0
        features = source.getFeatures()

        for current, feature in enumerate(features):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break

            # Add a feature in the sink
            sink.addFeature(feature, QgsFeatureSink.FastInsert)

            # Update the progress bar
            feedback.setProgress(int(current * total))

        # To run another Processing algorithm as part of this algorithm, you can use
        # processing.run(...). Make sure you pass the current context and feedback
        # to processing.run to ensure that all temporary layer outputs are available
        # to the executed algorithm, and that the executed algorithm can send feedback
        # reports to the user (and correctly handle cancellation and progress reports!)
        if False:
            buffered_layer = processing.run("native:buffer", {
                'INPUT': dest_id,
                'DISTANCE': 1.5,
                'SEGMENTS': 5,
                'END_CAP_STYLE': 0,
                'JOIN_STYLE': 0,
                'MITER_LIMIT': 2,
                'DISSOLVE': False,
                'OUTPUT': 'memory:'
            }, context=context, feedback=feedback)['OUTPUT']

        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        '''
        return {self.PASTA: pasta_saida}
