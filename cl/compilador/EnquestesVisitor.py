# Generated from Enquestes.g by ANTLR 4.7.2
from antlr4 import *

from models import Enquesta, Item, Alternativa, OpcioAlternativa, Pregunta, Resposta, OpcioResposta

if __name__ is not None and "." in __name__:
    from .EnquestesParser import EnquestesParser
else:
    from EnquestesParser import EnquestesParser


class EnquestesVisitor(ParseTreeVisitor):
    ids = {}  # Guardar los ids con sus objetos
    types = {
        'ENQUESTA': [],
        'PREGUNTA': [],
        'RESPOSTA': [],
        'ITEM': [],
        'ALTERNATIVA': []
    }

    def update_refs(self):
        for i in self.types['ITEM']:
            item = self.ids[i]
            self.ids[i].set_pregunta(self.ids[item.get_pregunta().get_id()])
            self.ids[i].set_resposta(self.ids[item.get_resposta().get_id()])
        for i in self.types['ALTERNATIVA']:
            alter = self.ids[i]
            self.ids[i].set_origen(self.ids[alter.get_origen().get_id()])
            alters = []
            for a in alter.get_alternativas():
                dest = self.ids[a.get_destino().get_id()]
                a.set_destino(dest)
                alters.append(a)
            self.ids[i].set_alternativas(alters)
        for i in self.types['ENQUESTA']:
            items = self.ids[i].get_items()
            new_items = []
            for item in items:
                new_items.append(self.ids[item.get_id()])
            self.ids[i].set_items(new_items)

    # Visit a parse tree produced by EnquestesParser#root.
    def visitRoot(self, ctx: EnquestesParser.RootContext):
        expr = self.visit(ctx.expr())
        self.update_refs()
        return {
            'objetos': self.ids,
            'tipos': self.types
        }

    # Visit a parse tree produced by EnquestesParser#text_token.
    def visitText_token(self, ctx: EnquestesParser.Text_tokenContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by EnquestesParser#string.
    def visitString(self, ctx: EnquestesParser.StringContext):
        text_token = ctx.text_token().getText()
        string = ctx.string()
        result = ''
        if string:
            result = self.visit(string) + ' ' + text_token
            return result
        else:
            return text_token

    # Visit a parse tree produced by EnquestesParser#pregunta.
    def visitPregunta(self, ctx: EnquestesParser.PreguntaContext):
        return self.visit(ctx.string()) + '?'

    # Visit a parse tree produced by EnquestesParser#expr_preg.
    def visitExpr_preg(self, ctx: EnquestesParser.Expr_pregContext):
        id = ctx.ID().getText()
        pregunta = self.visit(ctx.pregunta())
        if id in self.ids:
            preg = Pregunta(id=id, item=self.ids[id],
                            pregunta=pregunta, preguntada=self.ids[id])
        else:
            preg = Pregunta(id=id, pregunta=pregunta)
        self.ids[id] = preg
        self.types['PREGUNTA'].append(id)
        return preg

    # Visit a parse tree produced by EnquestesParser#only_resp.
    def visitOnly_resp(self, ctx: EnquestesParser.Only_respContext):
        return OpcioResposta(value=int(ctx.NUM().getText()), resposta=self.visit(ctx.string()))

    # Visit a parse tree produced by EnquestesParser#respuestas.
    def visitRespuestas(self, ctx: EnquestesParser.RespuestasContext):
        resps = ctx.respuestas()
        resposta = self.visit(ctx.only_resp())
        if resps:
            respostes = self.visit(resps)
            respostes.append(resposta)
            return respostes
        else:
            return [resposta]

    # Visit a parse tree produced by EnquestesParser#expr_resp.
    def visitExpr_resp(self, ctx: EnquestesParser.Expr_respContext):
        id = ctx.ID().getText()
        contenido = self.visit(ctx.respuestas())
        if id in self.ids:
            resp = Resposta(id=id, respostes=contenido, resposta=self.ids[id])
        else:
            resp = Resposta(id=id, respostes=contenido)
        self.ids[id] = resp
        self.types['RESPOSTA'].append(id)
        return resp

    # Visit a parse tree produced by EnquestesParser#item.
    def visitItem(self, ctx: EnquestesParser.ItemContext):
        relacion = []
        for n in ctx.ID():
            relacion.append(n.getText())
        return {
            'PREGUNTA': relacion[0],
            'RESPOSTA': relacion[1]
        }

    # Visit a parse tree produced by EnquestesParser#expr_item.
    def visitExpr_item(self, ctx: EnquestesParser.Expr_itemContext):
        id = ctx.ID().getText()
        contenido = self.visit(ctx.item())
        id_preg = contenido['PREGUNTA']
        if id_preg in self.ids:
            preg = Pregunta(id=id_preg, preguntada=self.ids[id_preg])
        else:
            preg = Pregunta(id=id_preg)
        id_resp = contenido['RESPOSTA']
        if id_resp in self.ids:
            resp = Resposta(id=id_resp, resposta=self.ids[id_resp])
        else:
            resp = Pregunta(id=id_resp)
        if id in self.ids:
            item = Item(id=id, item=self.ids[id],
                        pregunta=preg,
                        resposta=resp)
        else:
            item = Item(id=id, pregunta=preg,
                        resposta=resp)
        self.ids[id] = item
        self.types['ITEM'].append(id)
        return item

    # Visit a parse tree produced by EnquestesParser#assoc.
    def visitAssoc(self, ctx: EnquestesParser.AssocContext):
        value = int(ctx.NUM().getText())
        id = ctx.ID().getText()
        if id in self.ids:
            destino = Item(id=id, item=self.ids[id])
        else:
            destino = Item(id=id, item=self.ids[id])
        self.ids[id] = destino
        return OpcioAlternativa(value=value, destino=destino)

    # Visit a parse tree produced by EnquestesParser#list_assoc.
    def visitList_assoc(self, ctx: EnquestesParser.List_assocContext):
        lista_assoc = ctx.list_assoc()
        alternativa = self.visit(ctx.assoc())
        if lista_assoc:
            alternatives = self.visit(lista_assoc)
            if alternativa not in alternatives:
                alternatives.append(alternativa)
            return alternatives
        else:
            return [alternativa]

    # Visit a parse tree produced by EnquestesParser#alter.
    def visitAlter(self, ctx: EnquestesParser.AlterContext):
        origen = ctx.ID().getText()
        if origen in self.ids:
            item = Item(id=origen, item=self.ids[origen])
        else:
            item = Item(id=origen)
        self.ids[origen] = item
        data = self.visit(ctx.list_assoc())
        return {
            'origen': item,
            'data': data
        }

    # Visit a parse tree produced by EnquestesParser#alter_expr.
    def visitAlter_expr(self, ctx: EnquestesParser.Alter_exprContext):
        id = ctx.ID().getText()
        alternativas = self.visit(ctx.alter())
        origen = alternativas['origen']
        if id in self.ids:
            alt = Alternativa(id=id, origen=origen, alternativas=alternativas['data'], alternativa=self.ids[id])
        else:
            alt = Alternativa(id=id, origen=origen, alternativas=alternativas['data'])
        preg_id = origen.get_pregunta().get_id()
        if preg_id in self.ids:
            preg = Pregunta(id=preg_id, preguntada=self.ids[preg_id])
        else:
            preg = Pregunta(id=preg_id)
        preg.add_alternativas(alt)
        self.ids[preg_id] = preg
        self.ids[id] = alt
        self.types['ALTERNATIVA'].append(id)
        return alt

    # Visit a parse tree produced by EnquestesParser#encuesta.
    def visitEncuesta(self, ctx: EnquestesParser.EncuestaContext):
        data = ctx.encuesta()
        id_item = ctx.ID().getText()
        if data:
            items = self.visit(data)
            if id_item in self.ids:
                item = Item(id=id_item, item=self.ids[id_item])
            else:
                item = Item(id=id_item)
            items.append(item)
            return items
        else:
            if id_item not in self.ids:
                item = Item(id=id_item)
            else:
                item = Item(id=id_item, item=self.ids[id_item])
            self.ids[id_item] = item
            self.types['ITEM'].append(id_item)
            return [item]

    # Visit a parse tree produced by EnquestesParser#expr_enq.
    def visitExpr_enq(self, ctx: EnquestesParser.Expr_enqContext):
        id = ctx.ID_E().getText()
        items = self.visit(ctx.encuesta())
        if id not in self.ids:
            enq = Enquesta(id=id, items=items)
        else:
            enq = Enquesta(id=id, items=items, enquesta=self.ids[id])
        self.ids[id] = enq
        self.types['ENQUESTA'].append(id)
        return enq

    # Visit a parse tree produced by EnquestesParser#expr.
    def visitExpr(self, ctx: EnquestesParser.ExprContext):
        return self.visitChildren(ctx)


del EnquestesParser
