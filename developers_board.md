## Nov goals:
1. Cassan 2008 parametrization
2. triple lens use cases
3. FSPL for large rho with LD (Lee+09)
4. Binary source - allow setting flux ratio for all datasets in given band 


## Specific tasks to be performed
**boldfaced** tasks are most important because requested by the users

_italics_ mark important tasks

* Install
  * _makefile for Windows (basic instructions exist already)_
  * PIP install - the problem is that CustomInstall from setup.py is run when the archive is prepared, not when it's run on users machine; [link 1](https://packaging.python.org/tutorials/packaging-projects/), [link 2](https://setuptools.readthedocs.io/en/latest/setuptools.html)
  * setup.py should use Extensions instead of custom makefile
  * in setup.py in setup() add keywords: long\_description, classifiers
  * virtualenv; pip install -r requirements.txt; its best to install the dependencies first
  * more metadata in setup.py
* Documentation
  * Sagan workshop hands-on activity in MM
  * _examples as ipython notebooks_
  * Add \_\_repr\_\_ functions to Lens and Source
  * files not yet well documented: 
    * RA & Dec in coordinates.py (maybe also code it better)
    * coordinates.py
    * utils.py 
    * modelparameters.py
    * _Event.fit seems to be not documented_
  * Include full documentation via setup.py data\_files mechanism.
  * note that all plotting functions require plt.show() or plt.save()
  * try removing Attributes from docstrings - just make short @property functions
  * "Do not change values in results of this function." - change, because it's not a function
  * add a note that pi_E is "geocentric" (and "heliocentric" has the same length of vector but rotetated)
  * _list of all magnification methods_
  * _tutorial on model types_
  * _example 8 corrections - PSBL, not PSPL; clarify removing the anomaly_
  * _Event Arguments docstring_
  * make sure that website shows correct version of MM
* Effects:
  * **Binary source - see documents/binary\_source\_notes.md**:
    * finish use cases
    * _source\_flux\_ratio added to ModelParameters_
    * Fit.fit\_fluxes docstring to be updated
    * which\_parameters() - note that it doesn't work for binary source parameters, but the parameters work properly; just BSPL and rho_2 etc. are optional
    * models with fixed no blending: fit\_blending keyword changes
    * flux ratio - for band and for a list of datasets and both fixed and via regression
    * parallax models
    * binary source - there should be one Fit less in Event.get\_chi2xxx functions - if there are 2 sources, then calculate magnification and use F\_S = F\_S\_1+F\_S\_2 and get it from self.model.fit; most probably adding some function to Fit would help
    * binary lens binary source
    * different t\_E for each source (correct Model.set\_times)
    * test binary source with exactly one rho_X defined
  * Finite Source
    * FSPL with low magnification - do [Witt & Mao 94](http://adsabs.harvard.edu/abs/1994ApJ...430..505W) or [Witt 95](http://adsabs.harvard.edu/abs/1995ApJ...449...42W) give the right formulas?
    * FSPL ray shooting (ala getmag\_rs\_single.f)
    * Yoo+04 full formalism 
    * get gamma/u LD coeffs from Claret papers etc.
    * full formalism of [Lee+09](http://adsabs.harvard.edu/abs/2009ApJ...695..200L)
    * [Lee+09] - gradient calculations for uniform source
  * Xallarap (see below for references)
  * Quadratic limb darkening
  * Multi-lens ray shooting:
    * mapmaking version which adds new rays as needed (but remember that it runs for fixed (s,q) only!)
    * Yossi's idea to find all the images
  * Orbital motion like in [VBBL 2.0](https://arxiv.org/abs/1805.05653)
  * _Magnification function provided by the user - already started in user\_method branch; also this could be used to model variable source events - note that_
  * calculate jerk parallax degeneracy: [Park+04](http://adsabs.harvard.edu/abs/2004ApJ...609..166P) [Gould 04](http://adsabs.harvard.edu/abs/2004ApJ...606..319G)  
  * topocentric/Earth parallax
  * Chang-Refsdal binary calculations
  * elliptical source magnification [Heyrovsky & Loeb 1997](http://adsabs.harvard.edu/abs/1997ApJ...490...38H)
  * magnification calculated for a set of points, not just a trajectory - this way we could, e.g., plot magnification maps
  * fit\_blending for only some of the datasets
* Parameterization
  * Cassan 2008 binary lens parameters:
    * Cassan 2010 - Eq. 23, 24 and 25 - multiply s_in,s_out so that prior is uniform in (alpha,u0)
    * option to change scaling (from [0,1] to C08 params) to work well near topology change
  * [Albrow et al. 1999](http://adsabs.harvard.edu/abs/1999ApJ...522.1022A) (also Cassan 2008 Sec. 5)
  * t\_eff as a parameter - see [Andy's paper](https://arxiv.org/abs/1312.6692) and maybe also other from [Jen's 2012 paper](http://adsabs.harvard.edu/abs/2012ApJ...755..102Y), i.e., f\_lim=f\_s/u\_0 and q\*t\_E
  * caustic size w [Dong+09](http://adsabs.harvard.edu/abs/2009ApJ...698.1826D) refers to [Chung+05](http://adsabs.harvard.edu/abs/2005ApJ...630..535C)
  * check if new parameters are defined here: [Liebig, D'Ago, Bozza, and Dominik 2015](http://adsabs.harvard.edu/abs/2015MNRAS.450.1565L)
  * [Heyrovsky 2003](http://adsabs.harvard.edu/abs/2003ApJ...594..464H) parametrization of limb-darkening
  * t\_0\_planet, u\_0\_planet, t\_E\_planet instead of s, q, alpha
  * [Dominik 2009](http://adsabs.harvard.edu/abs/2009MNRAS.393..816D) for PSPL
* Function Improvements/Expansion:
  * BinaryLens class:
    * should BinaryLens() accept source\_x/y as lists or arrays?
    * function for center of mass shift (currently: shift\_x in trajectory.py, x\_shift in binarylens.py, xcm\_offset in caustics.py)
    * topology of caustics based on (s,q) - already is inside the Cassan+08 calculations, mostly needs use case
    * central and planetary caustic properties: [Chung et al. 2005](http://adsabs.harvard.edu/abs/2005ApJ...630..535C) and [Han 2006](http://adsabs.harvard.edu/abs/2006ApJ...638.1080H)
    * consider using Utils.complex\_fsum() in BinaryLens functions: \_polynomial\_roots\_ok\_WM95() and \_jacobian\_determinant\_ok\_WM95()
    * faster hexadecapole using [Cassan 2017](http://adsabs.harvard.edu/abs/2017MNRAS.468.3993C) ([code](https://github.com/ArnaudCassan/microlensing/blob/master/microlensing/multipoles.py))
    * _VBBL2.0 - are we using accuracy limit as default? If so then we should switch to relative accuracy_
  * Caustics class:
    * Caustics.\_calculate - optimize using vectors instead of a loop
    * _Caustics calculations using [Erdl & Schneider 1993](http://adsabs.harvard.edu/abs/1993A%26A...268..453E) approach_
    * root solver can be used the same as in binarylens.py - not needed for binary lens and Erdl & Schneider 1993
    * smaller points
  * Event class:
    * Event should sync information on which of the 3 types of parallax are used, so that if it's specified for event, then there will be exception if one dataset is missing earth\_coords etc. In general there should be some way to make sure which parallax types are used in which calculation of magnification. 
    * Class Event should have not only set\_datasets() methods but also add\_datasets(), i.e. a similar method that appends datasets to self.\_datasets.
    * **Allow fluxes to be fixed in chi^2 calculation (e.g. given a particular fs, fb, which you might want to do if you want fs as a chain parameter); also think how it will work for binary sources**
    * **give access to all fluxes without changing data\_ref**
    * reduce calls to Fit.fit\_fluxes()
    * add finite source in chi2\_gradient()
    * chi2\_gradient() should cope NaN values in a way similar to get\_chi2()
    * check all functions that should pass fit\_blending parameter
    * chi2 with maximum value provided - if the chi2 for point-source gives chi2 larger than specified limit, then finite source calculations are not undertaken (this should significantly speed-up MultiNest)
    * get flux and its error in reference system
    * get\_ref\_fluxes() - add fit\_blending=False option (also in Model class)
    * change order to improve the website
    * for consistency, it would be good to combine get\_chi2\_for\_dataset() and get\_chi2\_per\_point()
  * Fit class:
    * should use marginalized distributions of fluxes (if those are from linear fits); JCY - it needs UC
    * n\_sources somehow inconsistent in different places
  * Horizons class:
    * JPL Horizons
      * correct JPL Horizons => CSV file format; also example usage
      * check if Horizons e-mail is for correct satellite
    * BJD
      * conversions to BJD from HJD, JD etc. ([astropy link](http://docs.astropy.org/en/stable/time/#barycentric-and-heliocentric-light-travel-time-corrections))
      * BJD\_TDB in satellite ephemeris [astropy link](http://docs.astropy.org/en/stable/time/#barycentric-and-heliocentric-light-travel-time-corrections)
  * Lens class:
    * \_\_repr\_\_ function needs work                                         
    * a\_proj, couples with source distance in mulensmodel to determine s.  
    * 2-body example 3 is missing s. Why? Does that work?                  
    * problem with tracking number of masses, esp when successively defining masses (see test\_Lens.py)
    * implement triple+ systems  
  * MagnificationCurve class:
    * re-write magnification() to use lazy loading (here or in model.py)
  * Model class:
    * reorder functions so that it looks good on website
    * Model.set\_parameters() should remember previously set values (of course unless they're overwritten)
    * Class Model should not allow accessing attributes that shouldn't be there, eg., q for single lens case.
    * Function that prints RA, Dec, t\_0\_par, t\_0\_kep, types of parallaxes turned on, satellite info, limb coeffs and textual description of type of model
    * plot\_trajectory() - mark epochs using colorscale? Maybe it should be passed by kwargs (if so, then add example)
    * Should get\_satellite\_coords() use caching?
    * we should have versions of all plot functions to use magnifications instead of magnitudes; also add access via Event
    * set\_datasets() - check input
    * add option to use random zorder when plotting multiple datasets (e.g. gaussian with sigma depending on number of plotted datapoints)
    * **in functions magnification(), plot\_magnification(), and plot\_trajectory() use satellite\_skycoord from \_\_init\_\_ if available**
    * **plot\_lc() - add satellite option like in plot\_magnification(), other options as well** - use keywords passed to self.magnification()
    * does Model.plot\_lc() give docstring for flux\_ratio\_constraint option? If not, then present it in plot\_magnification() docstring
    * use pl.axhline() to plot 0 line in residuals plots at the end, using t\_min,t\_max
    * get\_residuals needs unit test
    * plot\_trajectory - mark data epochs (as pyplot kwargs use MulensData.plot\_properties)
    * plot\_caustics() - check if model has > 1 lens? or just plot a point for single lens
    * plot\_data & plot\_residuals - if color is not set by the user and show\_bad is True, then X-s are plotted using different color
    * _data\_ref lacks docstring_
  * ModelParameters class:
    * Transform t\_E and other parameters between geocentric and heliocentric frames.
    * option to return alpha, dalpha\_dt, and ds\_dt as floats instead of astropy.quantities
    * why .rho returns None if it's not defined? In other similar cases we have KeyError. Should that be changed? (if so, then maybe only after changing version to 2.0.0)
    * to make \_check\_valid\_combination\_1\_source shorter, make a boolean dict that says if given parameter is defined or not
    * change order to improve the website
    * _values in dimensionless astropy.quantity should be changed to float, other types should be rejected (unless it's a time unit etc.)_
    * _LaTeX strings with parameters names (useful e.g. for corner plots)_
    * check if t\_eff and t\_star can be used as input simultaneously
    * check if input values are floats (or something else accepted)
  * MulensData class:
    * **Errorbar scaling, in particular the two parameter.**
    * add version of n\_epochs that uses only good epochs
    * read settings from file header: flux vs. mag, filter, satellite info
    * change order to improve the website
    * docstring phot\_fmt vs. input\_fmt
    * data\_and\_err\_in\_input\_fmt() and Fit.get\_input\_format() possible can be deprecated or removed because we shifted to chi2\_fmt instead of input\_fmt
    * when plotting data, make sure that max/min limits on Y axis include errorbars, if the errorbars are shown
    * export/save given data file in scale of other dataset and model
  * PointLens class:
    * get\_pspl\_magnification() - change it to operate on u^2, not u, so that np.sqrt() calls are reduced
    * 1+2/u^4 approximation for very large u
    * improve the b0b1 tables so that relative interpolation errors are below 1e-5
  * SatelliteSkyCoord class:
    * attach magnification\_methods to SatelliteSkyCoord so that they overwrite Model and MagnificationCurve settings when given SatelliteSkyCoord is used
  * Trajectory class:
    * _\_get\_delta\_satellite() should be using self.times_
    * annual parallax caching - if moved to MulensData, then would be faster because hashing of coords and time vector takes time
    * maybe Trajectory should be able to plot itself, and Model.plot\_trajectory() should call it - it would be easier for binary sources etc.
    * colorscale time or magnification (see Ranc+ paper on ob151670)
  * Utils class:
    * in np.any() ifs give more information in warning e.g., "out of 1234 values provided, the fails are: 12, 345, 678 (0-based)"
    * add u(a) function: u = np.sqrt(2A/np.sqrt(A^2-1.) - 2.)
    * utils.py:57 - code produces 2 warnings, should produce just one; use masking
    * documentation - use ITALICS
    * uses masks there if warnings and apply None etc. - check examples after change!
  * MulensObjects submodule:
  * Plotting:
    * for plotting functions option to pass pyplot.Axis and pyplot.Figure instances and call e.g. Axis.scatter() instead of pyplot.scatter(); for a simple example see [here](https://github.com/rpoleski/K2-CPM/blob/master/source/K2CPM/plot_utils.py)
    * subplots with shared X-axis (plt.subplots(2, 1, sharex=True, gridspec\_kw={'height\_ratios': [4, 1]}, figsize=???, dpi=100)) - start in Example 5
    * add option to plot satellite coordinates as in Henderson+16 where K2 and Spitzer orbits were compared
    * add plotting with fit\_blending=False for functions that use magnitude space
    * add plt.xlim() and ylim in plotting functions (using t\_start) etc.; then also update (simplify) tutorials, examples etc.
    * rotate the trajectory, caustics, and critical curve plots so that the motion of the source is in general along X-axis - similar to Skowron+11 paper
    * caustics for trajectory plot with single lens models
  * Examples:
    * **chi2 per dataset**
    * **scipy.curve\_fit() and print parameter uncertainties**
    * add example that shows 'log\_' in the name of the parameter; central caustic anomaly planet would be best,
    * add illustration on how to remove airmass trends
    * add example of fitting PSPL model using [Albrow (2004)](http://adsabs.harvard.edu/abs/2004ApJ...607..821A) method [link](https://github.com/MichaelDAlbrow/SingleLensFitter/blob/master/SingleLensFitter.py)
    * **corner plots; they require [corner](https://github.com/dfm/corner.py), [pyhdust](https://github.com/danmoser/pyhdust), or [pyGTC](https://pypi.org/project/pyGTC/)**
    * _F\_s for MOA data for MB08310 differs from Janczak paper - is it caused by FSPL vs. FSBL models?_
    * plotting - sharex where possible
    * note in PSPL tutorial about plotting data in MulensData
  * Miscellaneous:
    * add function to get Earth's projected velocity
    * when checking units use Unit.physical\_type - search for physical\_type in mulensobjects/lens.py as an example; to find places to be changed search for "isinstance" (to find these places run grep isinstance \*py mulensobjects/\*py | grep Quantity
    * use lazy loading in MagnificationCurve.magnification and/or Model.magnification
    * guessing parameters of PSPL model ([Kim+17](https://arxiv.org/abs/1703.06883) as an example)
    * add calculation of Caustic Region of Influence (CROIN) - [Penny 2014](http://adsabs.harvard.edu/abs/2014ApJ...790..142Y)
    * anything from use cases that does not work yet -- see TODO.md file
    * interaction with fitting routines - see [list of them](https://arxiv.org/abs/1711.03329)
    * caching of results in trajectory.py should stop at some point - if the user changes t\_0\_par or coords, then there is no point in remembering huge indexes (whole self.times)
    * profile the code (python -m cProfile script.py)
    * Leap seconds library - [barycorrpy](https://arxiv.org/abs/1801.01634)
    * go to [documents/TODO.md](documents/TODO.md) file and check use cases listed there
* Other Tests:
  * add unit tests for Horizons and MulensData.satellite\_skycoord
  * Coordinates - write tests, possibly remove test\_Coords.py
  * t\_eff is not tested
  * plt.scatter -> plt.plot; after that we can start unit tests for plt calls
* Style/Architecture:
  * Are we consistent with PEP8? [check here](http://pep8online.com/) - last time fully checked on 28 Feb 2018 (but didn't include tests)
  * better import of the module so that all main classes are accessible (use \_\_all\_\_ = [...] in all files?)
  * Utils - Make subpackage/submodules that group related functions (e.g. flux2mag conversions)?

### reStructuredText:
[1st tutorial] (http://gisellezeno.com/tutorials/sphinx-for-python-documentation.html)

[2nd tutorial](http://www.sphinx-doc.org/en/stable/rest.html)

[example](https://thomas-cokelaer.info/tutorials/sphinx/docstring_python.html)

### Xallarap references:

[Griest & Hu 1992](http://adsabs.harvard.edu/abs/1992ApJ...397..362G),
[Han & Gould 1997](http://adsabs.harvard.edu/abs/1997ApJ...480..196H),
[Dominik 1998](http://adsabs.harvard.edu/abs/1998A%26A...329..361D),
[Ghosh et al. 2004](http://adsabs.harvard.edu/abs/2004ApJ...615..450G),
[Jiang et al. 2004](http://adsabs.harvard.edu/abs/2004ApJ...617.1307J)

ob9919 - [Smith et al. 2002](http://adsabs.harvard.edu/abs/2002MNRAS.336..670S)

[Poindexter et al. 2005](http://adsabs.harvard.edu/abs/2005ApJ...633..914P) - 23% of events are affected by xallarap

ob07368 - [Sumi et al. 2010](http://adsabs.harvard.edu/abs/2010ApJ...710.1641S) and [Suzuki et al. 2016](http://adsabs.harvard.edu/abs/2016ApJ...833..145S)

mb10328 - [Furusawa et al. 2013](http://adsabs.harvard.edu/abs/2013ApJ...779...91F)

ob150845 = mb15277 - Calen leads

