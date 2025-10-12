def load_scaled_image(pygame, path, target_width, target_height):
    original = pygame.image.load(path)
    orig_width, orig_height = original.get_size()
    
    # Вычисляем масштаб с сохранением пропорций
    scale = min(target_width / orig_width, target_height / orig_height)
    new_size = (int(orig_width * scale), int(orig_height * scale))
    
    return pygame.transform.scale(original, new_size)