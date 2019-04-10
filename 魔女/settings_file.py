class Settings():
	
	def __init__(self):
	
		#帧数
		self.fps_number = 45

		#背景音乐
		self.music = True

		#开始界面的背景色
		self.start_groundcolor = (220,220,220)
		
		#开始字体的颜色
		self.start_font_color = (100,90,100)	
		
		#设置界面点击框的颜色
		self.setting_rect_color = (100,90,100)
		
		#正常情况下的游戏中背景色
		self.playing_groundcolor = (245,235,225)

		#score字的颜色 矢车菊的蓝色
		self.score_color = (100,149,237)
		self.die_score_color = (30,30,30)
		
		#死亡后字显示颜色
		self.die_rect_color = (255,255,255)
		

		
		#屏幕大小
		self.screen_width=900
		self.screen_height=600	
		self.little_obj_distance = 1100		
		
		#游戏地图大小
		self.world_width = 3000
		self.world_height = 3000
	
		#怪物血条的颜色
		self.blood_rect_color = (250,100,100)
		self.blood_rect_color_red = (150,10,10)
		
		#魔法泉描述文字的颜色
		self.magic_words_color = (77,77,160)
		self.stain_remind_words_color = (33,33,140)
		
		#主角的出厂配置
		self.init_power = 1.2
		self.init_accelerated_speed = 0.1
		self.init_friction = -0.12
		self.init_blood = 200		
		self.init_max_blood = 200
		self.init_magic = 800
		self.init_max_magic = 1000
		
		
		