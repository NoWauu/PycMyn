"""module de définition des classes principales"""
from typing import List, Any, Tuple, Dict, Callable
import pygame

from modules.outils import dichotomie, forme_mask, UNIT_SIZE

pygame.init()

# constantes

POLICE = pygame.font.SysFont('Arial', 20)

# fonctions


def vect2_to_tuple(vecteur: pygame.Vector2):
    """convertie un vecteur2 en tuple d'entier"""
    return round(vecteur.x), round(vecteur.y)

# classes


class Sequence:
    """classe de gestion des séquences"""
    sequences: List['Sequence'] = []

    def __init__(self, seq: List[Tuple[Tuple[Callable[..., None], List[Any]] | None, float]], loop: bool = False, local: bool = False) -> None:

        self.fnct: List[Tuple[Callable[..., None], List[Any]] | None] = []
        self.times: List[float] = []
        self.is_running = False
        self.sqc_timer = pygame.time.get_ticks()
        self.pointer = 0
        self.loop = loop
        self.local = local

        self.pause_seq: Sequence | None = None

        for elm in seq:
            self.fnct.append(elm[0])
            self.times.append(elm[1])

        if local:
            Sequence.sequences.append(self)

    def start(self):
        """commence la séquence"""
        self.is_running = True
        self.pointer = 0
        self.sqc_timer = pygame.time.get_ticks()

    def fin(self):
        """met fin à la séquence"""
        self.is_running = False

    def pause(self, temps: int):
        """effectue une pause dans la séquence"""
        self.is_running = False
        self.pause_seq = Sequence(
            [((lambda: setattr(self, 'is_running', True), []), temps)])
        self.pause_seq.start()

    def step(self):
        """met à jour la séquence"""
        if self.pause_seq is not None and self.pause_seq.is_running:
            self.pause_seq.step()
            return False

        if not self.is_running or (self.times[self.pointer] >
                                   pygame.time.get_ticks() - self.sqc_timer):
            return False

        fnct = self.fnct[self.pointer]
        if fnct is not None:
            fnct[0](*fnct[1])
        self.pointer += 1
        self.sqc_timer = pygame.time.get_ticks()

        if self.pointer >= len(self.times):
            if self.loop:
                self.start()
            else:
                self.is_running = False
        return True

    def destroy(self):
        """détruit la séquence"""
        Sequence.sequences.remove(self)
        del self

    @classmethod
    def update(cls):
        """mise à jour de toutes les séquences"""
        a_detruire: List['Sequence'] = []
        for seq in cls.sequences:
            seq.step()
            if seq.local and not seq.is_running:
                a_detruire.append(seq)

        while len(a_detruire) > 0:
            a_detruire[0].destroy()
            a_detruire.pop(0)


class Interface:
    """classe de représentation des Interfaces"""
    current_interface: 'Interface'
    interfaces: Dict[str, 'Interface'] = {}

    def __init__(self, nom: str | None = None) -> None:
        self.elements: List['Element'] = []

        if nom is not None:
            Interface.interfaces[nom] = self

    def add_element(self, element: 'Element'):
        """ajoute un élément à la liste"""
        index: int = dichotomie(
            [elm.pos.z for elm in self.elements], element.pos.z)
        self.elements.insert(index, element)
        element.interface = self

    def remove_element(self, element: 'Element'):
        """retire un élément de la liste"""
        self.elements.remove(element)

    def on_keypress(self, event: pygame.event.Event):
        """gère les touches appuyées"""
        for elm in self.elements:
            if hasattr(elm.objet, 'on_keypress'):
                elm.objet.on_keypress(event)

    def on_click(self, event: pygame.event.Event):
        """gestion des cliques"""
        for elm in self.elements:
            if elm.enabled and hasattr(elm.objet, 'on_click'):
                elm.objet.on_click(event)

    def on_video_resize(self):
        """réaction au changement de la taille de la fenêtre"""
        for elm in self.elements:
            if hasattr(elm.objet, 'on_video_resize'):
                elm.objet.on_video_resize()

    def update(self):
        for elm in self.elements:
            if hasattr(elm, 'objet') and hasattr(elm.objet, 'update'):
                elm.objet.update()
            if hasattr(elm, 'update'):
                elm.update()

    def render(self):
        """méthode d'affichage"""
        return (elm.render() for elm in self.elements)

    @classmethod
    def add_element_to(cls, element: 'Element', interface_nom: str):
        """ajoute un élément à l'interface donnée"""
        if interface_nom in cls.interfaces:
            cls.interfaces[interface_nom].add_element(element)

    @classmethod
    def change_interface(cls, interface_nom: str):
        """change l'interface actuelle"""
        if interface_nom in cls.interfaces:
            cls.current_interface = cls.interfaces[interface_nom]


class Element:
    """
    classe de représentation
    d'un élément graphique
    """

    def __init__(self, objet: Any, surface: pygame.Surface, rectangle: pygame.Rect,
                 interface_nom: str | None = None, need_forming: bool = False) -> None:
        self.need_forming = need_forming
        self.surface = surface
        self.mask = (forme_mask(surface, UNIT_SIZE)
                     if need_forming else pygame.mask.from_surface(surface))
        self.rect = rectangle
        self.objet = objet
        self.backup_rotation = 0
        self.pos: pygame.Vector3 | RelativePos = self.objet.pos
        self.interface: Interface

        self.enabled = True

        if interface_nom is None:
            Interface.current_interface.add_element(self)
        else:
            Interface.add_element_to(self, interface_nom)

        self.update()

    def delie(self):
        """délie l'élément"""
        self.interface.remove_element(self)

    def able(self, *, able: bool = True):
        """active l'élément"""
        self.enabled = able

    def ancre(self):
        """ancre le rectangle à la bonne position"""
        # cas où l'élément n'est pas encore lié
        self.pos: pygame.Vector3 | RelativePos = self.objet.pos
        ancre = 'topleft'

        if isinstance(self.pos, RelativePos):
            ancre = self.pos.aligne

        self.rect.center = vect2_to_tuple(self.pos.xy)
        if 'top' in ancre:
            self.rect.top = vect2_to_tuple(self.pos.xy)[1]
        elif 'bottom' in ancre:
            self.rect.bottom = vect2_to_tuple(self.pos.xy)[1]
        if 'left' in ancre:
            self.rect.left = vect2_to_tuple(self.pos.xy)[0]
        elif 'right' in ancre:
            self.rect.right = vect2_to_tuple(self.pos.xy)[0]

    def update(self):
        """methode de mise à jour"""
        if isinstance(self.pos, RelativePos):
            self.pos.update()
        self.ancre()

        if hasattr(self, 'objet') and hasattr(self.objet, 'rotation'):
            # en degrés
            self.surface = pygame.transform.rotate(
                self.surface, self.objet.rotation - self.backup_rotation)
            self.backup_rotation = self.objet.rotation
        self.mask = (forme_mask(self.surface, UNIT_SIZE) if self.need_forming
                     else pygame.mask.from_surface(self.surface))

    def render(self):
        """méthode d'affichage"""
        return (self.surface, self.rect) if self.enabled else (pygame.Surface((0, 0)), pygame.Rect(0, 0, 0,0))


class Frame:
    """
    classe de représentation d'un groupement
    d'élément dans un cadre
    """

    frames: Dict[str, 'Frame'] = {}

    def __init__(self, nom: str, interface: Interface, surface: pygame.Surface, pos: 'pygame.Vector3 | RelativePos', interface_nom: str | None = None) -> None:
        self.surface = surface
        self.rect = self.surface.get_rect()
        self.pos = pos
        self.interface = interface
        self.element = Element(self, surface, self.rect, interface_nom, False)

        if nom not in Frame.frames:
            Frame.frames[nom] = self

    def on_keypress(self, event: pygame.event.Event):
        """gestion des touches"""
        self.interface.on_keypress(event)

    def update(self):
        """méthode de mise à jour"""
        # clear
        self.surface.fill('#000000')
        self.interface.update()
        self.surface.blits(list(self.interface.render()))


class RelativePos:
    """
    classe de représentation
    des positions variables
    """
    window: pygame.Surface

    def __init__(self, relx: float, rely: float, posz: int, aligne: str = 'centre') -> None:
        self.relx, self.rely = relx, rely
        self.x: float
        self.y: float
        self.xy: pygame.Vector2
        self.z = posz
        self.aligne = aligne
        self.update()

    def update(self):
        """méthode de mise à jour"""
        self.x = self.relx * RelativePos.window.get_width()
        self.y = self.rely * RelativePos.window.get_height()

        self.xy = pygame.Vector2(self.x, self.y)


class StaticElement(Element):
    """création d'un modèle immuable"""

    def __init__(self, objet: Any, surface: pygame.Surface, mask: pygame.Mask | None = None, interface_nom: str | None = None) -> None:
        super().__init__(objet, surface, surface.get_rect(), interface_nom, mask is None)
        self.ancre()
        if mask is not None:
            self.mask = mask

    def update(self):
        """surécrit la méthode pour la désactiver"""
        ...


class AnimElement(Element):
    """classe de gestion des animations"""

    def __init__(self, objet: Any, default_texture: pygame.Surface,
                 textures: Dict[str, List[Tuple[pygame.Surface, float]]],
                 interface_nom: str | None = None) -> None:
        """infos: temps en millisecondes"""
        self.default_texture = default_texture
        self.textures = textures

        self.current_texture: pygame.Surface = self.default_texture

        self.seq = Sequence([])

        super().__init__(objet, self.default_texture,
                         self.default_texture.get_rect(), interface_nom, True)

    def set_current_texture(self, texture: pygame.Surface):
        """change la texture utilisée"""
        self.current_texture = texture

    def reset_anim(self):
        """reset les animations"""
        self.seq.fin()

    def start_anim(self, nom: str):
        """déclenche une animation"""
        self.seq = Sequence(
            [((self.set_current_texture, [tpl[0]]), tpl[1]) for tpl in self.textures[nom]])
        self.seq.start()

    def check_next_anim(self) -> Tuple[pygame.Surface, bool]:
        """si le temps lié à l'animation est écoulé,
        passe à la texture suivante"""
        change = False
        if self.seq.is_running:
            change = self.seq.step()
        else:
            change = self.current_texture != self.default_texture
            self.current_texture = self.default_texture
        return self.current_texture, change

    def update(self):
        """méthode de mise à jour"""
        texture, change = self.check_next_anim()
        if change:
            self.surface = texture
            self.backup_rotation = 0
            self.rect = texture.get_rect()

        super().update()


class Bouton:
    """classe de représentation d'un bouton"""

    def __init__(self, pos: pygame.Vector3 | RelativePos, surface: pygame.Surface, fnct: Callable[[], None],
                 interface_nom: str | None = None, click: int = 1) -> None:
        self.pos = pos
        self.element = Element(
            self, surface, surface.get_rect(), interface_nom, False)
        self.fnct = fnct
        self.click = click

    def on_click(self, event: pygame.event.Event):
        """active lors du clique"""
        if self.element.rect.collidepoint(event.pos) and self.click == event.button:
            self.fnct()


class Texte:
    """gestion des textes"""

    def __init__(self, pos: pygame.Vector3 | RelativePos, texte: str = "", couleur: str = "#FFFFFF",
                 background_couleur: str = "#000000", interface_nom: str | None = None, scale: int = 1) -> None:
        self.pos = pos
        self.texte = texte
        self.couleur = couleur
        self.background_couleur = background_couleur
        self.scale = scale
        surface = POLICE.render(
            self.texte, True, self.couleur, self.background_couleur)
        surface = pygame.transform.scale_by(surface, self.scale)
        self.element = Element(
            self, surface, surface.get_rect(), interface_nom)

    def update(self):
        """mise à jour"""
        surface = POLICE.render(
            self.texte, True, self.couleur, self.background_couleur)
        surface = pygame.transform.scale_by(surface, self.scale)
        self.element.surface = surface
        self.element.rect = surface.get_rect()
