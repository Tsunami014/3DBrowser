from typing import Iterable
import pygame
from functools import lru_cache
from OpenGL.GL import *  # noqa: F403

def tex_coord(x, y, n=4):
    """Calculate texture coordinates for a given (x, y) position in an n x n texture atlas."""
    m = 1.0 / n
    dx, dy = x * m, y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m

@lru_cache
def loadTexture(name, nearest=False):
    """Load and configure a texture from an image file."""
    textureSurface = pygame.transform.flip(pygame.image.load(f'textures/{name}.png'), True, False)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width, height = textureSurface.get_size()

    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    # Set texture parameters for wrapping and filtering
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    if nearest:
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    else:
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glGenerateMipmap(GL_TEXTURE_2D)
    return texid

class Obj:
    def __init__(self, x, y, z, texture='noise'):
        self.x, self.y, self.z = x, y, z
        self.textureId = loadTexture(texture)

    tex_coords: Iterable[Iterable[float]]

    def verts(self) -> Iterable[Iterable[float]]:
        pass

    # Define edges for wireframe rendering
    edges: Iterable[Iterable[int]]
    """A tuple of indices referring to the verts() function, which returns the cube's corner points

    What idx of vertex (in the verts func) goes for each edge of the shape"""

    # Define surfaces for solid rendering
    surfaces: Iterable[Iterable[int]]
    """A tuple of indices referring to the verts() function, which returns the cube's corner points

    What idx of vertex (in the verts func) goes for each solid surface (face)"""

    def render(self):
        glBindTexture(GL_TEXTURE_2D, self.textureId)
        glBegin(GL_QUADS)
        block = self.tex_coords
        for i, surface in enumerate(self.surfaces):
            for j, vertex in enumerate(surface):
                glTexCoord2f(block[i][2*j], block[i][2*j+1])
                glVertex3fv(self.verts()[vertex])
        glEnd()
        
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.verts()[vertex])
        glEnd()

class Cube(Obj):
    @property
    def tex_coords(self):
        # Top, bottom, side*4
        return [tex_coord(0, 0), tex_coord(1, 0)] + [tex_coord(2, 0)] * 4

    def verts(self):
        # Return the 8 corner vertices of a cube centered at (x, y, z).
        return (
            (1+self.x, -1+self.y, -1+self.z), (1+self.x, 1+self.y, -1+self.z), (-1+self.x, 1+self.y, -1+self.z), (-1+self.x, -1+self.y, -1+self.z),
            (1+self.x, -1+self.y, 1+self.z), (1+self.x, 1+self.y, 1+self.z), (-1+self.x, -1+self.y, 1+self.z), (-1+self.x, 1+self.y, 1+self.z)
        )

    edges = ((0,1), (0,3), (0,4), (2,1), (2,3), (2,7), (6,3), (6,4), (6,7), (5,1), (5,4), (5,7))

    surfaces = ((0,1,2,3), (3,2,7,6), (6,7,5,4), (4,5,1,0), (1,5,7,2), (4,0,3,6))


class Flat(Cube):
    @property
    def tex_coords(self):
        # Top, bottom, side*4
        return [tex_coord(0, 0, 16), tex_coord(0, 0, 16), tex_coord(0, 0, 1)] + [tex_coord(0, 0, 16)] * 3
    
    def verts(self):
        return (
            (1+self.x, -1+self.y, -1+self.z), (1+self.x, 1+self.y, -1+self.z), (-1+self.x, 1+self.y, -1+self.z), (-1+self.x, -1+self.y, -1+self.z),
            (1+self.x, -1+self.y, self.z), (1+self.x, 1+self.y, self.z), (-1+self.x, -1+self.y, self.z), (-1+self.x, 1+self.y, self.z)
        )
