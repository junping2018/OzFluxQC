version_name = "OzFluxQC"
version_number = "V2.8.4"
# V2.8.4   - changes as follows:
#            - split gap filling into L4 (meteorological drivers) and
#              L5 (fluxes), partitioning is now L6
#            - associated changes to the template control files
#            - implemented gap filling from BIOS2
#            - implemented "Import" at L4 to allow importing MODIS data
#              into OzFluxQC data path
# V2.8.3   - implemented estimation of u* threshold by CPD (Barr et al)
# V2.8.2   - implemented;
#            - estimation of ecosystem respiration from nocturnal Fc
#              using SOLO and FFNET.
#            - several bug fixes
# V2.8.1   - refactor of gfACCESS_plotdetailed and associated code
# V2.8.0   - implemented;
#            - gap filling using ACCESS data (works for any alternate site file)
#            - menu at top of OzFluxQC GUI
# V2.7.2   - several enhancements, mainly to do with gap filling
#            - implemented "interpolated daily" method of
#              gap filling from climatology
#            - implemented gap filling at L3
# V2.7.1   - fixed bug in CorrectFcForStorage, Fc_storage_in typo
# V2.7.0   - major bug fixes as for V2.6.3 above
#          - minor bug fixes to clean up use of switches in ['Options'] section
#          - minor fixes to check that requested files exist
#          - implemented compare_ep.py to automate comparison of OzFluxQC and
#            EddyPro results
# V2.6.3 - clean up of code after comparing EddyPro and OzFluxQC
#          - fix bugs in mf.vapourpressure and mf.RHfromabsolutehumidity
#          - deprecated WPLcov after finding an error in Fc_WPLcov (units of wA term)
#          - rationalised calculation of dry and moist air densities and parial
#            density of water vapour
#          - implemented EddyPro method of calculating rho*Cp
#          - tidyied up use of densities in WPL correction and used flux
#            form (WPL80 Eqn 42a and 44) for Fe and Fc
#          - implemented EddyPro method of calculating Fh from Fhv
#          - rationalised use of densities and rho*Cp when calculating fluxes
# V2.6.2 - implement Lloyd-Taylor Reco
# V2.6.1 - fix 2D coordinate rotation for momentum covariances
# V2.6.0 - fix ConvertCO2 units bug
# V2.5.2 - implement sofm/solo/seqsolo
# V2.5.1 - post-Cairns 2013 version
