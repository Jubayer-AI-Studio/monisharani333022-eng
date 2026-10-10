import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

photo_path = 'C:/Users/ASSDI/.gemini/antigravity/brain/d575d19d-2024-413b-9428-b88fc2565794/.user_uploaded/media_1791176059548.jpg'
out_gif = 'C:/Users/ASSDI/.gemini/antigravity/scratch/monisharani333022-eng/assets/jubayer_live_banner.gif'
os.makedirs(os.path.dirname(out_gif), exist_ok=True)

orig_bgr = cv2.imread(photo_path)
H_orig, W_orig, _ = orig_bgr.shape

# Banner output dimensions: 1800 x 600
W_banner, H_banner = 1800, 600
scale = H_banner / H_orig
photo_w_scaled = int(W_orig * scale)

# Target coordinates in original photo:
# Editor code window: x: 655 to 795, y: 275 to 510
mon_x1, mon_x2 = 655, 795
mon_y1, mon_y2 = 275, 510
mon_w = mon_x2 - mon_x1
mon_h = mon_y2 - mon_y1

# Glasses reflection area: x: 440 to 580, y: 310 to 410
glass_x1, glass_x2 = 440, 580
glass_y1, glass_y2 = 310, 410

# Mug steam origin: x: 720, y: 555
mug_x, mug_y = 720, 555

# Prepare base dark background
bg_bgr = np.zeros((H_banner, W_banner, 3), dtype=np.float32)
for y in range(H_banner):
    r = 7.0 + (14.0 - 7.0) * (y / H_banner)
    g = 10.0 + (18.0 - 10.0) * (y / H_banner)
    b = 18.0 + (28.0 - 18.0) * (y / H_banner)
    bg_bgr[y, :, 0] = b # BGR
    bg_bgr[y, :, 1] = g
    bg_bgr[y, :, 2] = r

# Prepare feather mask for photo blending (smoothstep)
alpha_mask = np.ones((H_banner, photo_w_scaled), dtype=np.float32)
feather_w = int(photo_w_scaled * 0.44)
for x in range(feather_w):
    t_val = x / feather_w
    alpha_mask[:, x] = t_val * t_val * (3 - 2 * t_val)

for y in range(35):
    t_val = y / 35.0
    factor = t_val * t_val * (3 - 2 * t_val)
    alpha_mask[y, :] *= factor
    alpha_mask[H_banner - 1 - y, :] *= factor

alpha_3d = np.repeat(alpha_mask[:, :, np.newaxis], 3, axis=2)
photo_paste_x = W_banner - photo_w_scaled

# Code lines for monitor editor
raw_code = [
    'import { NoorAI } from \"@noorhub\";',
    'const jarvis = new Assistant({ os: \"win\" });',
    'await jarvis.initializeVoiceprint();',
    'const vision = await loadVisionEngine();',
    'if (vision.isStreaming) {',
    '  console.log(\"Hands-Free HUD: ACTIVE ⚡\");',
    '  await jarvis.listenAndExecute();',
    '}',
    'export const studio = new AI_Studio();',
    '// Status: 100% OPERATIONAL',
    'const db = drizzle(postgresClient);',
    'await db.syncTenants({ routeCount: 29 });',
    '// Build: SUCCESS - All tests passing'
]

font_code = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 12)
syntax_palette = [
    (198, 120, 221), # purple keyword
    (97, 175, 239),  # blue function
    (224, 108, 117), # red var
    (152, 195, 121), # green string
    (229, 192, 123), # yellow class
    (92, 99, 112)    # gray comment
]

# Typography fonts
font_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 72)
font_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 28)
font_badge = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16)
font_chip = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17)
font_bullet = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 20)
font_item_b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 19)
font_item_n = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 19)
try:
    code_watermark_font = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 240)
except:
    code_watermark_font = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 240)

left_margin = 90
pill_y = 80
pill_w = 400
pill_h = 36
name_y = 135
sub_y = 225
chip_y = 280
items_y = 345
line_y = H_banner - 45

chips = [
    ('Next.js 15', (14, 165, 233)),
    ('React 19', (56, 189, 248)),
    ('Python & FastAPI', (99, 102, 241)),
    ('Computer Vision', (168, 85, 247)),
    ('Autonomous AI', (236, 72, 153)),
    ('PostgreSQL', (16, 185, 129)),
]

bullets = [
    ('> ', 'Architect of NoorHub', ' — Universal Bilingual Education & Cloud SaaS (29 Routes)'),
    ('> ', 'Creator of Jubayer AI (Jarvis)', ' — 100% Hands-Free Voice, Vision & Gesture OS'),
    ('> ', 'Enterprise Automations', ' — Anti-Detection Scrapers, Content Bots & Video AI Pipelines')
]

NUM_FRAMES = 24
frames_pil = []

print(f'Rendering {NUM_FRAMES} high-fidelity cinemagraph frames...')

for f_idx in range(NUM_FRAMES):
    phase = f_idx / float(NUM_FRAMES)
    
    # 1. Modify Photo Layers in BGR
    frame_photo_bgr = orig_bgr.copy()
    
    # Code surface
    code_surface = Image.new('RGBA', (mon_w, mon_h), (24, 29, 41, 0))
    cs_draw = ImageDraw.Draw(code_surface)
    line_h = 18
    y_offset = -int(phase * (line_h * 2))
    
    for l_idx, line_txt in enumerate(raw_code):
        y_pos = y_offset + l_idx * line_h
        if -line_h <= y_pos <= mon_h:
            col = syntax_palette[l_idx % len(syntax_palette)]
            cs_draw.text((4, y_pos), line_txt, fill=col, font=font_code)
            if l_idx == 4 and (f_idx % 8 < 5):
                cursor_x = int(font_code.getbbox(line_txt)[2]) + 6
                cs_draw.rectangle([cursor_x, y_pos + 1, cursor_x + 3, y_pos + 13], fill=(56, 189, 248, 255))
    
    # Scanline
    scan_y = int(phase * mon_h)
    cs_draw.line([(0, scan_y), (mon_w, scan_y)], fill=(56, 189, 248, 110), width=2)
    
    code_np = np.array(code_surface)
    code_alpha = code_np[:, :, 3] / 255.0
    code_bgr = code_np[:, :, :3][:, :, ::-1]
    
    glow_mult = 1.0 + 0.15 * np.sin(2 * np.pi * phase)
    mon_roi = frame_photo_bgr[mon_y1:mon_y2, mon_x1:mon_x2].astype(np.float32)
    for c in range(3):
        mon_roi[:, :, c] = mon_roi[:, :, c] * (1.0 - code_alpha * 0.75) + code_bgr[:, :, c] * (code_alpha * 0.75)
    mon_roi = np.clip(mon_roi * glow_mult, 0, 255)
    frame_photo_bgr[mon_y1:mon_y2, mon_x1:mon_x2] = mon_roi.astype(np.uint8)
    
    # Dynamic screen reflection on glasses & cheek
    glass_roi = frame_photo_bgr[glass_y1:glass_y2, glass_x1:glass_x2].astype(np.float32)
    blue_pulse = 1.0 + 0.10 * np.sin(2 * np.pi * phase)
    glass_roi[:, :, 0] = np.clip(glass_roi[:, :, 0] * blue_pulse, 0, 255)
    glass_roi[:, :, 1] = np.clip(glass_roi[:, :, 1] * (1.0 + 0.05 * np.sin(2 * np.pi * phase)), 0, 255)
    frame_photo_bgr[glass_y1:glass_y2, glass_x1:glass_x2] = glass_roi.astype(np.uint8)
    
    # Steam rising from coffee cup
    steam_layer = np.zeros((H_orig, W_orig, 3), dtype=np.float32)
    for p_i in range(3):
        steam_phase = (phase + p_i * 0.33) % 1.0
        s_y = int(mug_y - steam_phase * 42)
        s_x = int(mug_x + np.sin(steam_phase * 4 * np.pi) * 8 + p_i * 4)
        s_rad = int(4 + steam_phase * 8)
        s_alpha = int(40 * (1.0 - steam_phase))
        if s_alpha > 0 and 0 <= s_x < W_orig and 0 <= s_y < H_orig:
            cv2.circle(steam_layer, (s_x, s_y), s_rad, (240, 240, 255), -1)
    steam_layer = cv2.GaussianBlur(steam_layer, (15, 15), 0)
    frame_photo_bgr = np.clip(frame_photo_bgr.astype(np.float32) + steam_layer * 0.35, 0, 255).astype(np.uint8)
    
    # Resize photo to banner height
    photo_resized = cv2.resize(frame_photo_bgr, (photo_w_scaled, H_banner), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    
    # Alpha blend onto canvas via NumPy
    canvas_bgr = bg_bgr.copy()
    roi = canvas_bgr[:, photo_paste_x:photo_paste_x + photo_w_scaled]
    canvas_bgr[:, photo_paste_x:photo_paste_x + photo_w_scaled] = (
        roi * (1.0 - alpha_3d) + photo_resized * alpha_3d
    )
    
    # Convert canvas to RGB PIL Image for crisp typography and vector accents
    canvas_rgb = cv2.cvtColor(canvas_bgr.astype(np.uint8), cv2.COLOR_BGR2RGB)
    frame_img = Image.fromarray(canvas_rgb).convert('RGBA')
    f_draw = ImageDraw.Draw(frame_img)
    
    # Dot grid
    dot_layer = Image.new('RGBA', (W_banner, H_banner), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(dot_layer)
    for dx in range(50, 1150, 42):
        for dy in range(40, H_banner - 30, 42):
            d_draw.ellipse([dx - 1, dy - 1, dx + 1, dy + 1], fill=(255, 255, 255, 12))
    frame_img = Image.alpha_composite(frame_img, dot_layer)
    
    # Code Watermark '< / >'
    wm_layer = Image.new('RGBA', (W_banner, H_banner), (0, 0, 0, 0))
    w_draw = ImageDraw.Draw(wm_layer)
    w_draw.text((50, 170), '< / >', fill=(56, 189, 248, 12), font=code_watermark_font)
    frame_img = Image.alpha_composite(frame_img, wm_layer)
    
    f_draw = ImageDraw.Draw(frame_img)
    
    # Status Pill Frame
    f_draw.rounded_rectangle([left_margin, pill_y, left_margin + pill_w, pill_y + pill_h], radius=18, fill=(15, 23, 42, 220), outline=(51, 65, 85, 255), width=2)
    f_draw.text((left_margin + 44, pill_y + 8), 'LIVE WORKSPACE  •  SYSTEMS ARCHITECT', fill=(148, 163, 184, 255), font=font_badge)
    
    # Status Pulse Beacon
    pulse_rad = 5 + int(3.5 * (0.5 + 0.5 * np.sin(2 * np.pi * phase)))
    beacon_alpha = int(140 * (1.0 - (pulse_rad - 5) / 4.0))
    beacon_layer = Image.new('RGBA', (W_banner, H_banner), (0, 0, 0, 0))
    bl_draw = ImageDraw.Draw(beacon_layer)
    bl_draw.ellipse([left_margin + 20 - pulse_rad, pill_y + 18 - pulse_rad, left_margin + 20 + pulse_rad, pill_y + 18 + pulse_rad], outline=(16, 185, 129, beacon_alpha), width=2)
    bl_draw.ellipse([left_margin + 16, pill_y + 14, left_margin + 24, pill_y + 22], fill=(16, 185, 129, 255))
    frame_img = Image.alpha_composite(frame_img, beacon_layer)
    
    f_draw = ImageDraw.Draw(frame_img)
    
    # Header Name
    f_draw.text((left_margin + 2, name_y + 2), 'Jubayer Ahmad', fill=(2, 6, 23, 200), font=font_title)
    f_draw.text((left_margin, name_y), 'Jubayer Ahmad', fill=(248, 250, 252, 255), font=font_title)
    
    # Subtitle
    f_draw.text((left_margin, sub_y), 'Senior Full-Stack Software Engineer & AI Systems Architect', fill=(56, 189, 248, 255), font=font_sub)
    
    # Tech Chips
    cur_x = left_margin
    for label, col in chips:
        bbox = font_chip.getbbox(label)
        cw = (bbox[2] - bbox[0]) + 30
        ch = 32
        f_draw.rounded_rectangle([cur_x, chip_y, cur_x + cw, chip_y + ch], radius=16, fill=(15, 23, 42, 210), outline=(col[0], col[1], col[2], 120), width=1)
        f_draw.ellipse([cur_x + 10, chip_y + 12, cur_x + 18, chip_y + 20], fill=col)
        f_draw.text((cur_x + 24, chip_y + 7), label, fill=(226, 232, 240, 255), font=font_chip)
        cur_x += cw + 10
    
    # Feature Bullet items
    for i, (sym, bold_txt, norm_txt) in enumerate(bullets):
        y_pos = items_y + i * 36
        f_draw.text((left_margin, y_pos), sym, fill=(56, 189, 248, 255), font=font_bullet)
        f_draw.text((left_margin + 26, y_pos), bold_txt, fill=(241, 245, 249, 255), font=font_item_b)
        b_len = font_item_b.getbbox(bold_txt)[2]
        f_draw.text((left_margin + 26 + b_len, y_pos), norm_txt, fill=(148, 163, 184, 255), font=font_item_n)
    
    # Hairline Accent Line
    for x in range(left_margin, W_banner - 100):
        t_val = (x - left_margin) / (W_banner - 100 - left_margin)
        if t_val < 0.2:
            alpha = int(255 * (t_val / 0.2))
        elif t_val > 0.8:
            alpha = int(255 * ((1 - t_val) / 0.2))
        else:
            alpha = 255
        r_val = int(14 + (99 - 14) * t_val)
        g_val = int(165 + (102 - 165) * t_val)
        b_val = int(233 + (241 - 233) * t_val)
        f_draw.line([(x, line_y), (x, line_y + 1)], fill=(r_val, g_val, b_val, alpha))
    
    # Traveling Laser Pulse
    laser_x = int(left_margin + phase * (W_banner - 100 - left_margin))
    laser_layer = Image.new('RGBA', (W_banner, H_banner), (0, 0, 0, 0))
    ll_draw = ImageDraw.Draw(laser_layer)
    for l_rad in range(32, 0, -3):
        l_alpha = int(180 * (1.0 - (l_rad / 32.0)))
        ll_draw.ellipse([laser_x - l_rad, line_y - 2, laser_x + l_rad, line_y + 3], fill=(56, 189, 248, l_alpha))
    ll_draw.ellipse([laser_x - 6, line_y - 2, laser_x + 6, line_y + 3], fill=(255, 255, 255, 255))
    frame_img = Image.alpha_composite(frame_img, laser_layer)
    
    frames_pil.append(frame_img.convert('RGB'))

print('Generating unified master palette...')
# Use middle frame to extract rich master palette
master_palette_img = frames_pil[NUM_FRAMES // 2].quantize(colors=256, method=Image.Quantize.MAXCOVERAGE, dither=Image.Dither.NONE)

print('Quantizing all frames with unified palette...')
quantized_frames = [
    f.quantize(palette=master_palette_img, dither=Image.Dither.NONE)
    for f in frames_pil
]

print(f'Saving animated GIF to {out_gif}...')
quantized_frames[0].save(
    out_gif,
    save_all=True,
    append_images=quantized_frames[1:],
    duration=75,
    loop=0,
    optimize=True
)

file_size_mb = os.path.getsize(out_gif) / (1024 * 1024)
print(f'SUCCESS! jubayer_live_banner.gif generated ({file_size_mb:.2f} MB)!')
