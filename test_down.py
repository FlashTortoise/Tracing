import tortoise as t

inc = t.p.inclination


class Judge_inclination(t.Task):
    def __init__(self):
        super(SimpleTask, self).__init__()
		self.reference = int(inc.pitch())
		self.degree = []
		self.flag1 = False
		self.flag2 = False
    def step(self):
		target_degree = self.reference + 10
		current_degree = int(inc.pitch())
		if not self.flag1:
			self.flag1 = test_up(current_degree,target_degree)
		elif not self.flag2:
			self.flag2 = test_down(current_degree,self.reference)
		
        print '{}, {}'.format(inc.pitch(), inc.roll())

def test_up(current_degree,target_degree):
	if current_degree > target_degreen:
		return True
	else:
		return False
		

def test_down(current_degree,self.reference):
	if current_degree = self.reference
	print end
		return True
	else:
		return False
		
if __name__ == '__main__':
    tttt = t.Tortoise()
    tttt.task = SimpleTask()
    tttt.walk()
