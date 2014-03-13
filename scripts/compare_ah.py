import constants as c
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy
import os
import qcio
import qcplot
import qcutils
import statsmodels.api as sm
import sys
import time

nfig = 0
plotwidth = 10.9
plotheight = 7.5

cf = qcio.load_controlfile(path='../controlfiles')
if len(cf)==0: sys.exit()

fname = qcio.get_infilename_from_cf(cf)
if not os.path.exists(fname):
    print " compare_ah: Input netCDF file "+fname+" doesn't exist"
    sys.exit()

ds = qcio.nc_read_series(fname)
if len(ds.series.keys())==0: print time.strftime('%X')+' netCDF file '+fname+' not found'; sys.exit()
# get the site name
SiteName = ds.globalattributes['site_name']
# get the time step
ts = int(ds.globalattributes['time_step'])
# get the datetime series
DateTime = ds.series['DateTime']['Data']
# get the initial start and end dates
StartDate = str(DateTime[0])
EndDate = str(DateTime[-1])
# find the start index of the first whole day (time=00:30)
si = qcutils.GetDateIndex(DateTime,StartDate,ts=ts,default=0,match='startnextday')
# find the end index of the last whole day (time=00:00)
ei = qcutils.GetDateIndex(DateTime,EndDate,ts=ts,default=-1,match='endpreviousday')
DateTime = DateTime[si:ei+1]
print time.strftime('%X')+' Start date; '+str(DateTime[0])+' End date; '+str(DateTime[-1])
Hdh = ds.series['Hdh']['Data'][si:ei+1]
Month = ds.series['Month']['Data'][si:ei+1]

nrecs = len(DateTime)
nperhr = int(float(60)/ts+0.5)
nperday = int(float(24)*nperhr+0.5)
ndays = nrecs/nperday
nrecs=ndays*nperday

Ah_7500_name = str(cf['Variables']['Ah_7500'])
Ah_HMP_name = str(cf['Variables']['Ah_HMP'])
ah_7500_30min_1d,flag = qcutils.GetSeriesasMA(ds,Ah_7500_name,si=si,ei=ei)
ah_HMP1_30min_1d,flag = qcutils.GetSeriesasMA(ds,Ah_HMP_name,si=si,ei=ei)
# reject 7500 data when the difference between the 7500 and HMP absolute humidities
# is larger than 10% of the HMP value
#d = numpy.ma.abs(ah_7500_30min_1d - ah_HMP1_30min_1d)
#ah_7500_30min_1d = numpy.ma.masked_where(d>0.2*ah_HMP1_30min_1d,ah_7500_30min_1d)
month_30min_1d,flag = qcutils.GetSeriesasMA(ds,'Month',si=si,ei=ei)
ah_7500_30min_2d = numpy.ma.reshape(ah_7500_30min_1d,[ndays,nperday])
ah_HMP1_30min_2d = numpy.ma.reshape(ah_HMP1_30min_1d,[ndays,nperday])
month_30min_2d = numpy.ma.reshape(month_30min_1d,[ndays,nperday])

mask = numpy.ma.mask_or(ah_7500_30min_2d.mask,ah_HMP1_30min_2d.mask)  # mask based on dependencies, set all to missing if any missing
ah_7500_30min_2d = numpy.ma.array(ah_7500_30min_2d,mask=mask)         # apply the mask
ah_HMP1_30min_2d = numpy.ma.array(ah_HMP1_30min_2d,mask=mask)
month_30min_2d = numpy.ma.array(month_30min_2d,mask=mask)

month_daily_avg = numpy.ma.average(month_30min_2d,axis=1)
ah_7500_daily_avg = numpy.ma.average(ah_7500_30min_2d,axis=1)
ah_HMP1_daily_avg = numpy.ma.average(ah_HMP1_30min_2d,axis=1)
ah_7500_daily_std = numpy.ma.std(ah_7500_30min_2d,axis=1)
ah_HMP1_daily_std = numpy.ma.std(ah_HMP1_30min_2d,axis=1)
ah_7500_daily_max = numpy.ma.max(ah_7500_30min_2d,axis=1)
ah_HMP1_daily_max = numpy.ma.max(ah_HMP1_30min_2d,axis=1)
ah_7500_daily_min = numpy.ma.min(ah_7500_30min_2d,axis=1)
ah_HMP1_daily_min = numpy.ma.min(ah_HMP1_30min_2d,axis=1)

ah_avgdiff_daily = ah_7500_daily_avg - ah_HMP1_daily_avg
ah_stdratio_daily = ah_HMP1_daily_std/ah_7500_daily_std
ah_7500range_daily = ah_7500_daily_max - ah_7500_daily_min
ah_HMP1range_daily = ah_HMP1_daily_max - ah_HMP1_daily_min
ah_rangeratio_daily = (ah_HMP1_daily_max - ah_HMP1_daily_min)/(ah_7500_daily_max - ah_7500_daily_min)

DT_daily = DateTime[0:nrecs:nperday]
#Mnth_30min_2d = Mnth_30min_1d.reshape(ndays,nperday)

nfig = nfig + 1
fig = plt.figure(nfig,figsize=(plotwidth,plotheight))
plt.figtext(0.5,0.95,SiteName,horizontalalignment='center',size=16)
qcplot.tsplot(DT_daily,ah_7500_daily_avg,sub=[3,1,1],ylabel='Ah_7500')
qcplot.tsplot(DT_daily,ah_HMP1_daily_avg,sub=[3,1,2],ylabel='Ah_HMP_01')
qcplot.tsplot(DT_daily,ah_avgdiff_daily,sub=[3,1,3],ylabel='7500-HMP')

#nfig = nfig + 1
#fig = plt.figure(nfig,figsize=(plotwidth,plotheight))
#plt.figtext(0.5,0.95,SiteName,horizontalalignment='center',size=16)
#qcplot.tsplot(DT_daily,ah_7500_daily_max,sub=[6,1,1],ylabel='7500x')
#qcplot.tsplot(DT_daily,ah_HMP1_daily_max,sub=[6,1,2],ylabel='HMP1x')
#qcplot.tsplot(DT_daily,ah_7500_daily_min,sub=[6,1,3],ylabel='7500n')
#qcplot.tsplot(DT_daily,ah_HMP1_daily_min,sub=[6,1,4],ylabel='HMP1n')
#qcplot.tsplot(DT_daily,ah_7500range_daily,sub=[6,1,5],ylabel='7500r')
#qcplot.tsplot(DT_daily,ah_HMP1range_daily,sub=[6,1,6],ylabel='HMP1r')

#nfig = nfig + 1
#fig = plt.figure(nfig,figsize=(plotwidth,plotheight))
#plt.figtext(0.5,0.95,SiteName,horizontalalignment='center',size=16)
#qcplot.tsplot(DT_daily,ah_7500_daily_std,sub=[4,1,1],ylabel='Sd(Ah_7500)')
#qcplot.tsplot(DT_daily,ah_HMP1_daily_std,sub=[4,1,2],ylabel='Sd(Ah_HMP)')
#qcplot.tsplot(DT_daily,ah_stdratio_daily,sub=[4,1,3],ylabel='Sd(HMP)/Sd(7500)')
#qcplot.tsplot(DT_daily,ah_rangeratio_daily,sub=[4,1,4],ylabel='HMPr/7500r')

# daily regressions
slope = numpy.ones(ndays)
offset = numpy.zeros(ndays)
correl = numpy.ones(ndays)
number = numpy.zeros(ndays)
for i in range(0,ndays-1):
    x = ah_7500_30min_2d[i,:]
    y = ah_HMP1_30min_2d[i,:]

    mask = (x.mask)|(y.mask)
    x.mask = mask
    y.mask = mask
    x_nm = numpy.ma.compressed(x)
    x_nm = sm.add_constant(x_nm)
    y_nm = numpy.ma.compressed(y)
    if len(y_nm)>1:
        resrlm = sm.RLM(y_nm,x_nm,M=sm.robust.norms.TukeyBiweight()).fit()
        coefs = resrlm.params
        
        #coefs = numpy.ma.polyfit(x,y,1)
        r = numpy.ma.corrcoef(x,y)
        number[i] = numpy.ma.count(x)
        slope[i] = coefs[0]
        offset[i] = coefs[1]
        correl[i] = r[0][1]
        #print number[i],slope[i],correl[i]

#nfig = nfig + 1
#fig = plt.figure(nfig,figsize=(plotwidth,plotheight))
#plt.figtext(0.5,0.95,SiteName,horizontalalignment='center',size=16)
#slope2 = numpy.ma.masked_where(correl<0.95,slope)
#offset2 = numpy.ma.masked_where(correl<0.95,offset)
#qcplot.tsplot(DT_daily,slope,sub=[5,1,1],ylabel='Slope',colours=correl)
#qcplot.tsplot(DT_daily,slope2,sub=[5,1,2],ylabel='Slope(r>0.95)',colours=correl)
#qcplot.tsplot(DT_daily,offset,sub=[5,1,3],ylabel='Offset',colours=correl)
#qcplot.tsplot(DT_daily,offset2,sub=[5,1,4],ylabel='Offset(r>0.95)',colours=correl)
#qcplot.tsplot(DT_daily,number,sub=[5,1,5],ylabel='Number',colours=correl)

symbol = ['ro','bo','yo','r+','b+','y+','r*','b*','y*','r^','b^','y^']
monthlist = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
#nfig = nfig + 1
#fig = plt.figure(nfig,figsize=(plotwidth,plotheight))
#plt.figtext(0.5,0.95,SiteName,horizontalalignment='center',size=16)
##qcplot.xyplot(ah_HMP1_daily_avg,ah_diff_daily_avg,sub=[1,1,1],regr=1,title="Daily Average",xlabel='Ah_HMP (g/m3)',ylabel='7500-HMP (g/m3)')
#j = 0
#for i in [1,2,3,4,5,6,7,8,9,10,11,12]:
    #j = j + 1
    #index = numpy.where(month_daily_avg==i)[0]
    #if len(index)!=0:
        #x = ah_HMP1_daily_avg[index]
        #y = ah_avgdiff_daily[index]
        #plt.plot(x,y,symbol[i-1],label=monthlist[i-1])
        #plt.xlabel('Ah_HMP (g/m3)')
        #plt.ylabel('Ah_7500 - Ah_HMP (g/m3)')
    #plt.legend(loc=2,scatterpoints=0,frameon=False)

MnthList = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
nfig = nfig + 1
fig = plt.figure(nfig,figsize=(plotwidth,plotheight))
plt.figtext(0.5,0.95,SiteName,horizontalalignment='center',size=16)
j = 0
for i in [1,2,3,4,5,6,7,8,9,10,11,12]:
    j = j + 1
    index = numpy.where(month_30min_1d==i)[0]
    if len(index)!=0:
        y = ah_HMP1_30min_1d[index]
        x = ah_7500_30min_1d[index]
        if j in [1,2,3,4,5,6,7,8,9]:
            xlabel = None
        else:
            xlabel = '7500 (g/m3)'
        if j in [2,3,5,6,8,9,11,12]:
            ylabel = None
        else:
            ylabel = 'HMP (g/m3)'
        qcplot.xyplot(x,y,sub=[4,3,j],regr=2,title=MnthList[i-1],xlabel=xlabel,ylabel=ylabel)
plt.tight_layout()

nfig = nfig + 1
figts = plt.figure(nfig,figsize=(plotwidth,plotheight))
plt.figtext(0.5,0.95,SiteName,horizontalalignment='center',size=16)
qcplot.tsplot(DT_daily,correl,sub=[5,1,1],ylabel='Correl',colours=number)
qcplot.tsplot(DT_daily,number,sub=[5,1,2],ylabel='Number',colours=correl)
qcplot.tsplot(DT_daily,slope,sub=[5,1,3],ylabel='Slope',colours=correl)
qcplot.tsplot(DT_daily,offset,sub=[5,1,4],ylabel='Offset',colours=correl)
qcplot.tsplot(DT_daily,ah_stdratio_daily,sub=[5,1,5],ylabel='Sd(HMP)/Sd(7500)',colours=correl)

correl2 = numpy.ma.masked_where((correl<0.98)|(number<30),correl)
number2 = numpy.ma.masked_where((correl<0.98)|(number<30),number)
slope2 = numpy.ma.masked_where((correl<0.98)|(number<30),slope)
offset2 = numpy.ma.masked_where((correl<0.98)|(number<30),offset)
sdratio2 = numpy.ma.masked_where((correl<0.98)|(number<30),ah_stdratio_daily)
nfig = nfig + 1
figts = plt.figure(nfig,figsize=(plotwidth,plotheight))
plt.figtext(0.5,0.95,SiteName,horizontalalignment='center',size=16)
qcplot.tsplot(DT_daily,correl2,sub=[5,1,1],ylabel='Correl',colours=number)
qcplot.tsplot(DT_daily,number2,sub=[5,1,2],ylabel='Number',colours=correl)
qcplot.tsplot(DT_daily,slope2,sub=[5,1,3],ylabel='Slope',colours=correl)
qcplot.tsplot(DT_daily,offset2,sub=[5,1,4],ylabel='Offset',colours=correl)
qcplot.tsplot(DT_daily,sdratio2,sub=[5,1,5],ylabel='Sd(HMP)/Sd(7500)',colours=correl)

class PointBrowser:
    def __init__(self):
        self.ind_day = 0
        self.start_ind_day = 0
        self.ind_30min = 0
        self.start_ind_30min = 0
        self.end_ind = 0
        self.nfig = nfig
        self.slope = []
        self.offset = []
        self.correl = []
        self.start_date = []
        self.end_date = []
        self.stdratio = []
        self.rangeratio = []

    def onpress(self, event):
        if self.ind_day is None: return
        if event.key=='n': self.new()
        if event.key=='f': self.forward()
        if event.key=='b': self.backward()
        if event.key=='q': self.quitprog()
        if event.key not in ('n', 'f', 'b', 'q'): return

    def new(self):
        print 'Creating new XY plot ...'
        self.plotted = False
        self.nfig += 1
        self.figxy = plt.figure(self.nfig,figsize=(5,4))
        self.figxy.subplots_adjust(bottom=0.15,left=0.15)
        self.axxy = self.figxy.add_subplot(111)
        self.axxy.set_xlabel('Ah_7500 (g/m3)')
        self.axxy.set_ylabel('Ah_HMP (g/m3)')
        if self.ind_day!=0:
            self.start_date.append(DT_daily[self.start_ind_day])
            self.end_date.append(DT_daily[self.ind_day])
            self.slope.append(self.coefs[0])
            self.offset.append(self.coefs[1])
            self.correl.append(self.r[0][1])
            self.stdratio.append(numpy.ma.average(ah_stdratio_daily[self.start_ind_day:self.ind_day]))
            self.rangeratio.append(numpy.ma.average(ah_rangeratio_daily[self.start_ind_day:self.ind_day]))
            self.start_ind_day = self.ind_day
            self.ind_30min = DateTime.index(DT_daily[self.ind_day])
            self.start_ind_30min = self.ind_30min
        plt.show()

    def forward(self):
        self.ind_day += 1
        self.ind_day = numpy.clip(self.ind_day,0,len(DT_daily)-1)
        self.ind_30min = DateTime.index(DT_daily[self.ind_day])
        self.update()

    def backward(self):
        self.ind_day += -1
        self.ind_day = numpy.clip(self.ind_day,0,len(DT_daily)-1)
        self.ind_30min = DateTime.index(DT_daily[self.ind_day])
        self.update()

    def update(self):
        i = self.ind_30min
        x = ah_7500_30min_1d[self.start_ind_30min:i]
        y = ah_HMP1_30min_1d[self.start_ind_30min:i]
        self.axxy.cla()
        self.axxy.plot(x,y,'b.')
        self.axxy.set_xlabel('Ah_7500 (g/m3)')
        self.axxy.set_ylabel('Ah_HMP (g/m3)')
        mask = (x.mask)|(y.mask)
        x.mask = mask
        y.mask = mask
        x_nm = numpy.ma.compressed(x)
        x_nm = sm.add_constant(x_nm)
        y_nm = numpy.ma.compressed(y)
        self.r = numpy.ma.corrcoef(x_nm,y_nm)
        if (len(x_nm)>30)&(self.r[0][1]>0.98):
            resrlm = sm.RLM(y_nm,x_nm,M=sm.robust.norms.TukeyBiweight()).fit()
            self.coefs = resrlm.params
            y_fit = resrlm.fittedvalues
        else:
            y_fit = numpy.ma.array(x_nm,mask=True)

        self.axxy.plot(x_nm[:,0],y_fit,'r--',linewidth=3)
        eqnstr = 'y = %.3fx + %.3f, r = %.3f'%(self.coefs[0],self.coefs[1],self.r[0][1])
        self.axxy.text(0.5,0.875,eqnstr,fontsize=8,horizontalalignment='center',transform=self.axxy.transAxes)
        dtstr = str(DT_daily[self.start_ind_day]) + ' to ' + str(DT_daily[self.ind_day])
        self.axxy.text(0.5,0.925,dtstr,fontsize=8,horizontalalignment='center',transform=self.axxy.transAxes)
        self.figxy.canvas.draw()
            
        dtstr = str(DT_daily[self.start_ind_day]) + ' to ' + str(DT_daily[self.ind_day])
        self.axxy.text(0.5,0.925,dtstr,fontsize=8,horizontalalignment='center',transform=self.axxy.transAxes)
        self.figxy.canvas.draw()
        #eqnstr = 'y = %.3fx + %.3f'%(resrlm.params[0],resrlm.params[1])
        #plt.plot(x_nm[:,0],resrlm.fittedvalues,'r--',linewidth=3)
        #plt.text(0.5,0.9,eqnstr,fontsize=8,horizontalalignment='center',transform=ax.transAxes)

    def quitprog(self):
        self.start_date.append(DT_daily[self.start_ind_day])
        self.end_date.append(DT_daily[self.ind_day])
        self.slope.append(self.coefs[0])
        self.offset.append(self.coefs[1])
        self.correl.append(self.r[0][1])
        self.stdratio.append(numpy.ma.average(ah_stdratio_daily[self.start_ind_day:self.ind_day]))
        self.rangeratio.append(numpy.ma.average(ah_rangeratio_daily[self.start_ind_day:self.ind_day]))
        for i in range(len(self.slope)):
            eqnstr = '%.3f, %.3f, %.3f, %.3f, %.3f'%(self.slope[i],self.offset[i],self.correl[i],self.stdratio[i],self.rangeratio[i])
            print self.start_date[i], self.end_date[i], eqnstr
        plt.close('all')

browser = PointBrowser()

figts.canvas.mpl_connect('key_press_event', browser.onpress)

plt.show()
