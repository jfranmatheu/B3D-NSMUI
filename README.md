## New Sculpt Mode UI for Blender 2.80

# Downloads
- Download **NewSculptUI.zip** For original Blender 2.80 version: https://github.com/jfranmatheu/Blender_NewSMUI/raw/master/NewSculptUI.zip


- [Not updated / Just ignore] Download **NewSculptUI_SculptFeatures.zip** For support with Experimental Sculpt Branch of Pablo Dobarro: https://github.com/jfranmatheu/Blender_NewSMUI/raw/master/NewSculptUI_SculptFeatures.zip

[![Paypal](https://raw.githubusercontent.com/stefan-niedermann/paypal-donate-button/master/paypal-donate-button.png)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=johnnymathgar%40gmail.com&item_name=Soporte+para+el+desarrollo+continuado+de+addons+gratuitos.&currency_code=EUR&source=url)

Nueva UI para el modo Sculpt. Modifica principalmente el Tool Header del sculpt mode.

# FEATURES
---
QUICK TEXTURE CREATION AND SELECTION
---
**1ST.** BRUSH HASN'T A TEXTURE -
- If you don't have textures imported, click at '5' so you create a new empty texture
- Else -> Click at '4' and select one

![alt text](http://4.bp.blogspot.com/-IGoDgT9mGJQ/XOgZi-lan7I/AAAAAAAAAe0/v3FrLAScZK8nbzplJuS04rvxjSAma5ZUwCK4BGAYYCw/s400/NewSMUI_1.png "Texture Section 1")

**2ND.** SO THERE'S A TEXTURE AVAILABLE BUT IT HASN'T AN IMAGE!
- If you don't have images imported, click at '7' to import one
- Else -> Click at '6' and select one

![alt text](http://2.bp.blogspot.com/-ndXyh7GAp6g/XOgZi1KAq7I/AAAAAAAAAe4/UyzTHpqj96QyRrdTU_VhoPxvZNHJCM6MgCK4BGAYYCw/s400/NewSMUI_2.png "Texture Section 2")

**3RD.** NOW IT HAS BOTH IMAGE AND TEXTURE
- You can change their names at '8' and '9'
- You can select another image for that texture at '6'
- You can change quickly the texture of the actual brush at '4'

![alt text](http://1.bp.blogspot.com/-69waiwHKDig/XOgZiwh_BVI/AAAAAAAAAfE/0ixHWNBt-vAd391Bs5JKgV1j2h_BTj6ywCK4BGAYYCw/s320/NewSMUI_3.png "Texture Section 3")

1. Texture Settings
2. New Texture (just works if a texture is created)
3. Open image
4. Texture Quick Selector (1 step)
5. New texture button (conditional)
6. Image Quick Selector
7. Open Image (conditional)
8. Texture Name
9. Image Name

Differences between buttons 2/5 and 3/7:
- While '2' creates an empty texture
- '5' Create one and assign it to the active brush
- While '3' imports an image/multiple images
- '7' Imports one and assigns it to the active or selected texture
---

RENDER YOUR CUSTOM BRUSH ICONS! WITH JUST ONE CLICK!!!!!
---
### The process is just an instant but due to some changes in Blender internal, the icon preview may update in a couple of seconds... But not if you use the render button from collapse menu (which is active by default). So you dont have to wait til see the icon updated.
1. Toggle "Render Custom Brush Icon" (now it's in the "eye icon" drop down menu of the tool header) or toggle "collapse" option to access it from the dropdown menu near the brush selector over the tool header or toggle ''brush options'' in gear icon of the tool header (to access from the side "brushes" panel)
2. Pick your custom brush, make some strokes and zoom in and center the mesh to be ready for the shoot
3. Click at the camera icon of the tool header/panel (depends of [1.]), BOOM, now you have a custom icon for your brush
- NOTE: this is a very new feature so feedback and bug reports are needed to improve this powefull feature!
- If you want a custom icon with alpha (no background) you should go to layout workspace or any other because in Sculpting workspace this is not working well as expected

- GIF EXAMPLE - Activate Render Icon and Render icon (3 alternatives)

![alt text](https://1.bp.blogspot.com/-77lFR3HDL08/XR5AXe19blI/AAAAAAAAA1A/C486t8jLwy8ntnATPqEV3iBDcdW11TdowCLcBGAs/s640/ezgif.com-optimize.gif "Render Custom Brush Icon")

- GIF EXAMPLE - (by gen.es)

![alt text](http://4.bp.blogspot.com/-qh358q7MjJs/XQEBkCvsUWI/AAAAAAAAAlo/mhskAOlgnCoOFurdBTFtKRvsI0s45LaQQCK4BGAYYCw/s1600/pinceles.gif "Gif example")

---

DYNTOPO + QUICK 'DETAIL SIZE' SELECTOR [DEFAULT MODE]
---
- Try to activate the Stage Mode!!! It's a great improvement to the dyntopo and scultpting workflow :D

![alt text](http://4.bp.blogspot.com/-TWXG-spErQU/XPzRNix3jPI/AAAAAAAAAjU/g3N0ejbrePA6CnSCc72c_AeVNW4H56nowCK4BGAYYCw/s400/dyntopo_default.png "Dyntopo")
---

DYNTOPO NEW "STAGE" CONCEPT + NEW MENU [STAGE MODE]
---
![alt text](http://1.bp.blogspot.com/-tCsMLruKp7M/XPzYDNUOxRI/AAAAAAAAAjg/pxjg7LVn1AI0U0Z0-dWQhN0pQaPcIYTTACK4BGAYYCw/s400/dyntopo_stages.png "Dyntopo Stages")

---
NEW BRUSH SET PANELS !!!
---
## Favorite Brushes, Recent Brushes and Brushes per type !!!
https://blender.chat/file-upload/CjSzJWhscJngPC7m7/2019-06-15%2000-50-23.mp4

![alt text](http://4.bp.blogspot.com/-_y7dNWNuRaw/XRKRRameGAI/AAAAAAAAAzI/JS6PubqSnmEtKCMtPk9asmOwXp9HGe9ugCK4BGAYYCw/s1600/brushespanel.png "Brushes Panel")

- Panel is responsive !!
- All parts (preview, favs, per type, recent brushes... can be hidden! And replaced by Active Brush subpanel options)

![alt text](http://2.bp.blogspot.com/-w9z7EAwRkwA/XRKRRbKgSqI/AAAAAAAAAzE/Y8fX_rnAj0UY5DrzCRhMVd-QxnmCsSydACK4BGAYYCw/s320/brushespanelresponsive.png "Brushes Panel Responsive")

---
QUICK SYMMETRY
---
![alt text](http://4.bp.blogspot.com/-AQyygMd2kbo/XOgZi7420RI/AAAAAAAAAfA/f3e5ViEtS7oEIN1Z5TlMZkyYv8j-2oHSACK4BGAYYCw/s400/NewSMUI_symmetry.png "Symmetry")

---
BRUSHES
---
![alt text](http://3.bp.blogspot.com/-PQ7zUxZrncg/XOgZi2edKVI/AAAAAAAAAek/jUMv6gUiYJYmRbhCndKDCX6rF8ab-DMrgCK4BGAYYCw/s320/NewSMUI_brush.png "Brushes")

- Brush Options (collapsed options to a dropdown menu)

![alt text](http://3.bp.blogspot.com/-YNmdm-OwNeQ/XRKRRWJpjZI/AAAAAAAAAy4/vqoEV7MVfegvJqTsttLwasWHp7mdt_D5gCK4BGAYYCw/s320/brushoptions.pngg "Brush Options")

---
Brush Settings / Stroke Settings / Curves
---
![alt text](http://3.bp.blogspot.com/-VMm2vj-sXSE/XOgZiymhfnI/AAAAAAAAAfI/opiTVUUTAY8EPwCeoN6Vxy3lzulD4cwdACK4BGAYYCw/s320/NewSMUI_settings.png "Settings")

- Stroke Method, Now they have their own icons!

![alt text](http://3.bp.blogspot.com/-OLauVc4SGNE/XR47r_VHZMI/AAAAAAAAA0w/_kwNj-y3kS4WBJCEES_4XKgClsyZAwjeACK4BGAYYCw/s400/strokemethoddots.png "Stroke Method")

- Curve Presets! Now they are toggles so you know which one is active!!

![alt text](http://4.bp.blogspot.com/-WBZ4wA9vmco/XR47N39UfII/AAAAAAAAA0g/Uxol381Mee4xa0HswLCJ412n9ZM_www-ACK4BGAYYCw/s400/curvestoggles.png "Curve Presets")

---
MASKING
---
![alt text](http://3.bp.blogspot.com/-rUSzGjTz-Ps/XOgZi8H9P7I/AAAAAAAAAe8/y1Nssl4haHsnV4kJmB4NbNfpCw2kYWP7wCK4BGAYYCw/s400/NewSMUI_mask.png "Mask")

---
BRUSH SLIDERS (they all are activatable)
---
![alt text](http://1.bp.blogspot.com/-g5QFeNxN_RA/XOga3bJZxNI/AAAAAAAAAf0/JxUM67mqqqMwavQHcQvRWKIQ-rta5yCtACK4BGAYYCw/s320/NewSMUI_sliders.png "Sliders")
![alt text](http://2.bp.blogspot.com/-WZH5SsT3BC8/XPzlLbCKbrI/AAAAAAAAAkc/QDWwk8mxKvIOURQ-dbgsbkkUquC321MJgCK4BGAYYCw/s400/slider_spacing.png "Spacing")

---
CUSTOMIZE THE UI!!! :D  + PRESETS !! (CUSTOM PRESETS FOR FUTURE)
---
- Toggle UI Element, have only the UI elements that you really want!!!
- There are so much tools that are not showed by default but you can activate them with just only click :-)
- I recommend you to try "Render Custom Brush Icon", "Stroke Method" and "Curve Presets", also feedback for the UI is needed in order to have actived by default the most useful features.

![alt text](http://3.bp.blogspot.com/-wswIcW7wQDg/XR43DoHcIfI/AAAAAAAAA0E/fbU_tYLkM3cfoMbwgTM1xkFK2d8i3npSgCK4BGAYYCw/s1600/toggleUIElementss.png "Toggle UI Elements")

![alt text](http://1.bp.blogspot.com/--dwa0-Ue-tw/XRKRSJFot3I/AAAAAAAAAzQ/-hGAKQGyvaYJbJHaKaCux0ZshsUVPgYfgCK4BGAYYCw/s640/allfeaturestoolheader.png "All Features Tool Header")

---
QUICK PREFERENCES (ADDON CONFIG AND BLENDER PREFS)
---
![alt text](http://4.bp.blogspot.com/-dvZjOYxG-RQ/XR43D-qYGmI/AAAAAAAAA0I/TSnNv6u3Z8UWmpDPU1Y9AeV6rhrV4WpQACK4BGAYYCw/s1600/preferencesaddon.png "Preferences")

---
BRUSH SIZE, STRENGTH AND SMOOTH VALUE SHORTCUTS
---
RMB up-down and drag to increase/decrease brush size and brush strength
Also ALT + RMB and drag to increase/decrease autosmooth

![alt text](http://3.bp.blogspot.com/-NyBd_bUgZHE/XRKTZRIFQFI/AAAAAAAAAzo/8KDk8GPTbsEofzzQeMQzpS_gvIZkfhZUwCK4BGAYYCw/s320/PiLT8oPtT5.gif "Brush resize, strength and smooth shortcut")

---
CUSTOM ICONS
---
![alt text](http://4.bp.blogspot.com/-QOTH4wgMenI/XPVO9HooF-I/AAAAAAAAAg8/GNsISB9Rlpkz61XbmH-p3lKqIdm4EVaugCK4BGAYYCw/s640/icons.png "Icons")

---

FUTUROS CAMBIOS E IDEAS LOCAS
---
# Texturas etc:
- [x] Carga, creación y selección rápida de imágenes y texturas para el esculpido y para aplicar directamente sobre el pincel activo.
- [ ] Nuevo operador para si abres una imagen en una brocha sin textura asignada, que automáticamente cree una textura y asigne esa imagen a la textura (Sólo 1 paso!!!).
- [ ] Poder seleccionar **varias imágenes**, importarlas de golpe y que automáticamente se creen texturas con esas imágenes.
- [ ] Cuando importas una imagen para una textura, la textura cambiará el nombre al de la imagen de forma automática, esto (y en combinación con las 2 anteriores) ayudará a no perder el tiempo renombrando innecesariamente.

# Dyntopo etc:
- [x] Soporte para multires si se detecta un modificador 'Multiresolution'.
- [x] Nuevo concepto de 'Stages' donde poder dividir el proceso de esculpido según su workflow adecuado, Nuevo panel/menú dropdown para Dyntopo con esta nueva característica y valores predefinidos para cada 'stage' y para cada modo de detalle usado (relative, constant, brush), además del modo por defecto, es decir, sin usar stages, en el cual contaremos con 6 niveles de detalle predefinidos.
- [ ] Los valores predefinidos y el número de valores... serán personalizables! (modo edición para la edición de los valores).
- [ ] Mantener dyntopo activado al cambiar de modo.

# OTROS
- [x] Icono personalizados para la brocha seleccionada con solo un click, basado en la vista actual con un render.
- [ ] Insertar primitivas sin salir de sculpt, usando el 3dcursor con snap de superficie o de volumen y la normal de este para posicionarlo. SHIF + RMB
- [ ] Filtros para las texturas.
- [x] Sets de brochas: 1, Recientemente usadas. 2, Por tipo según la brocha activa. 3, Favoritas.
- [x] Nuevos y mejores atajos de teclado. Gracias al addon de Jean Ayer que he integrado podemos usar click derecho y arrastrar en uno de los axis (horizontal y vertical) para cambiar el tamaño o la fuerza de la brocha de forma fácil. Este ha sido mejorado, extendido y personalizado bastante especialmente para este addon.
- [x] Reestructuración en el código para hacerlo más limpio y además MODULAR.
- [x] Poder desactivar y activar diferentes elementos de la UI para un mayor nivel de personalización. Esto se hace desde el panel de la 'N' llamado "Sculpt".
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

# CREDITS
---
"brush quickset" addon by Jean Ayer aka Vrav
https://blenderartists.org/t/sculpt-paint-edit-workflow-suite-new-grow-sel-to-cursor/553819

Icons for dyntopo detailing (Relative, Brush and Constant + high, mid and low) made by g3n.es
