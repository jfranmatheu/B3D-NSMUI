# Blender_NewSMUI
New Sculpt Mode UI for Blender 2.80

Nueva UI para el modo Sculpt. Modifica principalmente el Tool Header del sculpt mode.


# FEATURES
---
QUICK TEXTURE CREATION AND SELECTION
---
**1ST.** BRUSH HASN'T A TEXTURE -
Now an empty texture is available and It will change to (next image)
- If you don't have textures imported, click at '5' and import one
- Else -> Click at '4' and select one

![alt text](https://github.com/jfranmatheu/just_images/blob/master/NewSMUI_1.png"Texture Section 1")

**2ND.** SO THERE'S A TEXTURE AVAILABLE BUT IT HASN'T AN IMAGE!
- If you don't have images imported, click at '7' to import one
- Else -> Click at '6' and select one

![alt text](https://github.com/jfranmatheu/just_images/blob/master/NewSMUI_2.png"Texture Section 2")

**3RD.** NOW IT HAS BOTH IMAGE AND TEXTURE
- You can change their names at '8' and '9'
- You can select another image for that texture at '6'
- You can change quickly the texture of the actual brush at '4'

![alt text](https://github.com/jfranmatheu/just_images/blob/master/NewSMUI_3.png"Texture Section 3")

1. Texture Settings
2. Duplicate/New Texture (just works if a texture is created)
3. Open image
4. Texture Quick Selector (1 step)
5. New texture button (conditional)
6. Image Quick Selector
7. Open Image (conditional)
8. Texture Name
9. Image Name

DYNTOPO + QUICK 'DETAIL SIZE' SELECTOR
---
![alt text](https://github.com/jfranmatheu/just_images/blob/master/NewSMUI_dyntopo.png"Dyntopo")

---
QUICK SYMMETRY
---
![alt text](https://github.com/jfranmatheu/just_images/blob/master/NewSMUI_symmetry.png"Symmetry")

---
BRUSHES
---
![alt text](https://github.com/jfranmatheu/just_images/blob/master/NewSMUI_brush.png"Brushes")

---
Brush Settings / Stroke Settings / Curves
---
![alt text](https://github.com/jfranmatheu/just_images/blob/master/NewSMUI_settings.png"Settings")

---
MASKING
---
![alt text](https://github.com/jfranmatheu/just_images/blob/master/NewSMUI_mask.png"Mask")

---
BRUSH PROPERTIES SLIDERS
---
![alt text](https://github.com/jfranmatheu/just_images/blob/master/NewSMUI_sliders"Sliders")

---
CUSTOM ICONS
---
![alt text](https://github.com/jfranmatheu/just_images/blob/master/NewSMUI_icons.png"Icons")

---

FUTUROS CAMBIOS E IDEAS LOCAS
---
# Para la zona de texturas:
- [ ] Nuevo operador para si abres una imagen en una brocha sin textura asignada, que automáticamente cree una textura y asigne esa imagen a la textura (Sólo 1 paso!!!).
- [ ] Poder seleccionar **varias imágenes**, importarlas de golpe y que automáticamente se creen texturas con esas imágenes.
- [ ] Cuando importas una imagen para una textura, la textura cambiará el nombre al de la imagen de forma automática, esto (y en combinación con las 2 anteriores) ayudará a no perder el tiempo renombrando innecesariamente.

# Para la zona de dyntopo:
- [ ] Los valores predefinidos para el 'Detail Size' de Dyntopo, serán colapsables o se podrán ocultar con algún ajuste (aún por decidir)
- [ ] Los valores predefinidos y el número de valores... serán personalizables!

# OTROS
- [ ] Filtros para las texturas.
- [ ] Sets de brochas: 1, Recientemente usadas. 2, Por tipo según la brocha activa. 3, Favoritas.
- [ ] Nuevos y mejores atajos de teclado.
- [ ] Manager para brochas.
- [ ] Nueva brocha personalizable con multitud de parámetros configurables.
- [ ] Exportación/Importación (1 click) de brochas.
- [ ] Preview grande del alpha o textura (en hover) en una esquina o lateral del 3d viewport.
- [ ] Mejora en la previsualización de las texturas en el thumbnail.
- [ ] Soporte para preview de los .psd
- [ ] Cambio fácil de icono de una brocha y soporte con greasepencil para hacer los diseños de los iconos.
- [ ] Añadir nuevas herramientas y más avanzadas para enmascarar.

- [ ] Empezar a desarrollar la UI para el texture paint mode.

# Soporte para las Sculpt Features (Pablo Dobarro)
Disponibles de momento en otra 'branch' -> Sculpt-Features
## Para el Header
- [x] [Color] Selector de color y check para el 'unified color' entre brochas
- [ ] [Remesher] Slider para el voxel size y botón para el remesh, o el botón de remesh y un dropdown menu con los ajustes.


