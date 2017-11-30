from glob import glob
import numpy as np
import random

class pairs():
	def __init__(self, imagesPath, noOfPositiveExamples, noOfNegativeExamples, imgExtension = "JPEG"):
		self.imagesPath = imagesPath				# path of a directory where are folders with images (each folder - different category)
		self.noOfPositiveExamples = noOfPositiveExamples	# number of positive ("same") examples per category
		self.noOfNegativeExamples = noOfNegativeExamples	# number of negative ("different") examples per category
		self.imgExtension = imgExtension

	def get_all_images_in_lists(self):
		self.images = []
		folderList = glob(self.imagesPath+'*/')
		for folder_i, folder in enumerate(folderList):
			imgPathList = glob(folder+'*'+self.imgExtension)
			self.images.append(imgPathList)
		self.noOfCategories = len(self.images)

	def get_random_two_images(self, listA, listB):
		imageA = np.random.choice(listA)
		imageB = np.random.choice(listB)
		# make sure they are not the same image:
		while(imageA==imageB):
			imageB = np.random.choice(listB)

		return imageA, imageB

	def create_pairs(self):
		pairsList = []
		for i in xrange(self.noOfCategories):
			print "Class", i+1,"out of", self.noOfCategories
			negativeCategoriesList = np.delete(np.arange(0,self.noOfCategories),i)
			for k in xrange(self.noOfPositiveExamples):
				imageA, imageB = self.get_random_two_images(self.images[i], self.images[i])
				pairsList.append([imageA,imageB,"1"])
			for k in xrange(self.noOfNegativeExamples):
				j = np.random.choice(negativeCategoriesList)
				imageA, imageB = self.get_random_two_images(self.images[i], self.images[j])
				pairsList.append([imageA,imageB,"0"])
		return pairsList

	def split_list_into_four_textfiles(self, pairsList):
		trainFileLeft = ""
		trainFileRight = ""
		valFileLeft = ""
		valFileRight = ""
		random.shuffle(pairsList)	# shuffle list of pairs
		for line in pairsList:
			# choose randomly if it's a val or train case (split 70/30):
			if(random.random()>0.3):
				trainFileLeft+= line[0]+" "+line[2]+"\n"
				trainFile2Right+= line[1]+" "+line[2]+"\n"
			else:
				valFileLeft+= line[0]+" "+line[2]+"\n"
				valFile2Right+= line[1]+" "+line[2]+"\n"
		f = open('./train_left.txt','w')
		f.write(trainFileLeft)
		f.close()
		f = open('./train_right.txt','w')
		f.write(trainFileRight)
		f.close()
		f = open('./val_left.txt','w')
		f.write(valFileLeft)
		f.close()
		f = open('./val_right.txt','w')
		f.write(valFileRight)
		f.close()
		
			
		
					

#------------------------------------------------------------------
def main():
	IMAGES_PATH = "/media/jedrzej/SAMSUNG/DATA/ILSVRC2012/TRAIN/"

	trainingPairsGenerator = pairs(IMAGES_PATH, 1000, 5000)
	trainingPairsGenerator.get_all_images_in_lists()
	pairsList = trainingPairsGenerator.create_pairs()
	trainingPairsGenerator.split_list_into_two_textfiles(pairsList)

if __name__ == "__main__":
    main()
