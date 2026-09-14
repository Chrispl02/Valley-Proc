      subroutine geobfield(tm,r,theta,phi,br,bt,bp,b)
c*****evaluate bfield at geocentric coords r,theta,phi
c     and return components of field in r,theta and phi directions
c     and magnitude
c*****theta and phi are in radians, r is in km, b is in gauss
c ===============================================================
c
c   essentially, this is an adaptation of igrfdemo. it interpolates
c   smoothly between the coefficients from 1945 to 1985.
c
c     subroutines:
c         getshc, interpshc, extrapshc, shval3
c
c     igrfdemo is due to:
c     a. zunde
c     usgs, ms 964, box 25046 federal center, denver, co  80225
c
c ===============================================================
      character*8 filmod(17)
c      character*31 fqual
      dimension gh1(220), gh2(220), gha(224), ext(3), dtemod(17)
      data ext /3*0./
      data filmod /  'dgrf45', 'dgrf50',
     1               'dgrf55', 'dgrf60', 'dgrf65',
     2               'dgrf70', 'dgrf75', 'dgrf80',
     3               'dgrf85', 'dgrf90', 'dgrf95',
     4               'dgrf00', 'dgrf05', 'dgrf10',
     5               'dgrf15', 'igrf20', 'igrf20s'/
c      data fqual/"/usr/local/lib/faraday/bfmodel/"/
      data dtemod / 1945., 1950., 1955., 1960.,
     1       1965., 1970., 1975., 1980., 1985., 1990., 1995., 2000.,
     2     2005.,2010.,2015.,2020.,2025./              
      data iu/98/,ndt/17/
c      data a2/40680925./, b2/40408588./
      data a2/40680631.6/, b2/40408296.0/ ! updated 2010
c
      data rtd/57.29577951/
      data tmp/0./,lp/0/
      character(1024) :: fqual_temp
      character(:), allocatable :: fqual
      call get_path(fqual_temp)
c      write(*,*) "L_BEF: ", fqual_temp, "L_BEF_end"
      fqual = TRIM(fqual_temp)
c      write(*,*) "L: ", fqual, "L_end"

      flat=90. - theta*rtd
      flon=rtd*phi
c*****if previous time is not equal to current time
      if(tm .ne. tmp)then
         l=0
C        for i=1,ndt
         DO  1010  i=1,ndt
C          exit for if(tm .lt. dtemod(i))
            if(tm .lt. dtemod(i)) GO TO  1011
            l=i
C        end for
 1010    CONTINUE
 1011    CONTINUE
c       write(*,-)tm,l
        if(l .eq. 0)then
           write(*,fmt='(" geobfield: time is before earliest model.")')
           stop
        end if
        if(l .eq. ndt)then
           l=l-1
           write(*,fmt='(" geobfield: warning - extrapolating beyond ",
     1                   "last set of coefficients.")')
        end if
        if(l .ne. lp)then
c*********if previous epoch not the same, read in new coefs
c         write(*,fmt='(" read coefs"))')
c          write(*,*) "filmod", fqual//filmod(l)
           call getshc2 (iu, fqual//filmod(l), nmax1, erad, gh1, ier)
c	   write(*,*) "AA: ", ier, filmod(l)
           if(ier .ne. 0)then
              write(*,fmt='(" geobfield: read error=",i2," on ",a)')
     1                   ier,filmod(l)
              stop
           end if

           call getshc2 (iu, fqual//filmod(l+1), nmax2, erad, gh2, ier)
          if(ier .ne. 0)then
             write(*,fmt='(" geobfield: read error=",i2," on ",a)')
     1            ier,filmod(l+1)
             stop
          end if
       end if
       if (l .lt. ndt-1) then
          call interpshc (tm, dtemod(l), nmax1, gh1, dtemod(l+1),
     1         nmax2, gh2, nmax, gha)
c         write(*,fmt='(" interpolate"))')
       else
          call extrapshc (tm, dtemod(l), nmax1, gh1, nmax2,
     1        gh2, nmax, gha)
c         write(*,fmt='(" extrapolate"))')
       end if
      end if
c      tmp=tm
c      lp=l
      call shval3(2,flat,flon,r,erad,a2,b2,nmax,gha,0,ext,x,y,z)
      br=-z/100000.
      bp=y/100000.
      bt=-x/100000.
      b=sqrt(br**2 + bp**2 + bt**2)

C      write(*,*)flat,flon,r,erad,a2,b2,nmax,gha,ext
C      write(*,*)tm,r,theta,phi,br,bt,bp,b
      return
      end
c
      subroutine convrt(i, gdlat, gdalt, gclat, rkm)
 
c     convrt converts between geodetic and geocentric coordinates. the
c     reference geoid is that adopted by the iau in 1964. a=6378.16,
c     b=6356.7746, f=1/298.25. the equations for conversion from
c     geocentric to geodetic are from astron. j., vol 66, 1961, p. 15.
 
c          i=1   geodetic to geocentric
c          i=2   geocentric to geodetic
c        gdlat   geodetic latitude (degrees)
c        gdalt   altitude above geoid (km)
c        gclat   geocentric latitude (degrees)
c          rkm   geocentric radial distance (km)
c
c      data   a/6378.16/,       ab2/1.0067397/,   ep2/.0067397/
c     update 2010
      data   a/6378.137/,       ab2/1.0067396/,   ep2/.0067396/
      data dtr/.0174532925199/
 
      if (i .eq. 1) then
 
c     .....geodetic to geocentric.....
 
         gdl    = dtr*gdlat
         sinlat = sin(gdl)
         coslat = cos(gdl)
         sl2    = sinlat*sinlat
         cl2    = ab2*coslat
         cl2    = cl2*cl2
         sinbet = sinlat/sqrt(sl2+cl2)
         sb2    = amin1(sinbet*sinbet, 1.)
         cosbet = sqrt(1. - sb2)
         rgeoid = a/sqrt(1. + ep2*sb2)
         x      = rgeoid*cosbet + gdalt*coslat
         y      = rgeoid*sinbet + gdalt*sinlat
         rkm    = sqrt(x*x + y*y)
         gclat  = atan2(y,x)/dtr
         return
 
      else if (i .eq. 2) then
 
c     .....geocentric to geodetic.....
 
         rer  = rkm/a
         a2   = ((-1.4127348e-8/rer + .94339131e-8)/rer +
     1           .33523288e-2)/rer
         a4   = (((-1.2545063e-10/rer + .11760996e-9)/rer +
     1           .11238084e-4)/rer - .2814244e-5)/rer
         a6   = ((54.939685e-9/rer - 28.301730e-9)/rer +
     1            3.5435979e-9)/rer
         a8   = (((320./rer - 252.)/rer + 64.)/rer - 5.)
     1            /rer*0.98008304e-12
         gcl  = dtr*gclat
         ccl  = cos(gcl)
         scl  = sin(gcl)
         s2cl  = 2.*scl*ccl
         c2cl  = 2.*ccl*ccl - 1.
         s4cl  = 2.*s2cl*c2cl
         c4cl  = 2.*c2cl*c2cl - 1.
         s8cl  = 2.*s4cl*c4cl
         s6cl  = s2cl*c4cl + c2cl*s4cl
         dltcl = s2cl*a2 + s4cl*a4 + s6cl*a6 + s8cl*a8
         gdlat = gclat + dltcl/dtr
         gdalt = rkm - a/sqrt(1.+ep2*scl*scl)
         return
 
      end if
      end
c
      subroutine getshc2 (iu, fspec, nmax, erad, gh, ier)
 
c ===============================================================
c
c      version 1.01
c
c      reads spherical harmonic coefficients from the specified
c      file into an array.
c
c      input:
c          iu    - logical unit number
c          fspec - file specification
c
c      output:
c          nmax  - maximum degree and order of model
c          erad  - earth's radius associated with the spherical
c                harmonic coefficients, in the same units as
c                elevation
c          gh    - schmidt quasi-normal internal spherical
c                harmonic coefficients
c          ier   - error number: =  0, no error
c                          = -2, records out of order
c                               = fortran run-time error number
c
c      a. zunde
c      usgs, ms 964, box 25046 federal center, denver, co  80225
c
c ===============================================================
 
      character      fspec*(*)
      dimension      gh(*)
      
c ---------------------------------------------------------------
c      open coefficient file. read past first header record.
c      read degree and order of model and earth's radius.
c ---------------------------------------------------------------

      
      open (iu, file=fspec, status='old', iostat=ier, err=999 )

 
      read (iu, *, iostat=ier, err=999)
      read (iu, *, iostat=ier, err=999) nmax, erad


c ---------------------------------------------------------------
c      read the coefficient file, arranged as follows:
c
c                              n     m     g     h
c                              ----------------------
c                            /   1     0    gh(1)  -
c                           /    1     1    gh(2) gh(3)
c                          /     2     0    gh(4)  -
c                         /      2     1    gh(5) gh(6)
c          nmax*(nmax+3)/2     / 2     2    gh(7) gh(8)
c             records          \ 3     0    gh(9)  -
c                         \      .     .     .     .
c                          \     .     .     .     .
c          nmax*(nmax+2)    \    .     .     .     .
c          elements in gh    \  nmax  nmax   .     .
c
c      n and m are, respectively, the degree and order of the
c      coefficient.
c ---------------------------------------------------------------
 
      i = 0
C      for nn = 1, nmax
      DO  1010  nn = 1, nmax
C          for mm = 0, nn
      DO  1020  mm = 0, nn
            read (iu, *, iostat=ier, err=999) n, m, g, h
c            write(*,*) n,m,g,h,nn,nmax,mm,ier
            if (nn .ne. n .or. mm .ne. m) then
                ier = -2
                goto 999
            endif
            i = i + 1
            gh(i) = g
            if (m .ne. 0) then
                i = i + 1
                gh(i) = h
            endif
C          end for
 1020 CONTINUE
 1021 CONTINUE
C      end for
 1010 CONTINUE
 1011 CONTINUE
 
999      close (iu)

      return
      end
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ bfieldsr  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
      subroutine interpshc (date, dte1, nmax1, gh1, dte2,
     1                        nmax2, gh2, nmax, gh)
 
c ===============================================================
c
c      version 1.01
c
c      interpolates linearly, in time, between two spherical
c      harmonic models.
c
c      input:
c          date  - date of resulting model (in decimal year)
c          dte1  - date of earlier model
c          nmax1 - maximum degree and order of earlier model
c          gh1   - schmidt quasi-normal internal spherical
c                harmonic coefficients of earlier model
c          dte2  - date of later model
c          nmax2 - maximum degree and order of later model
c          gh2   - schmidt quasi-normal internal spherical
c                harmonic coefficients of later model
c
c      output:
c          gh    - coefficients of resulting model
c          nmax  - maximum degree and order of resulting model
c
c      a. zunde
c      usgs, ms 964, box 25046 federal center, denver, co  80225
c
c ===============================================================
 
      dimension      gh1(*), gh2(*), gh(*)
 
c ---------------------------------------------------------------
c      the coefficients (gh) of the resulting model, at date
c      date, are computed by linearly interpolating between the
c      coefficients of the earlier model (gh1), at date dte1,
c      and those of the later model (gh2), at date dte2. if one
c      model is smaller than the other, the interpolation is
c      performed with the missing coefficients assumed to be 0.
c ---------------------------------------------------------------
 
      factor = (date - dte1) / (dte2 - dte1)
 
      if (nmax1 .eq. nmax2) then
          k = nmax1 * (nmax1 + 2)
          nmax = nmax1
      else if (nmax1 .gt. nmax2) then
          k = nmax2 * (nmax2 + 2)
          l = nmax1 * (nmax1 + 2)
C          for i = k + 1, l
      DO  1010  i = k + 1, l
            gh(i) = gh1(i) + factor * (-gh1(i))
C          end for
 1010 CONTINUE
 1011 CONTINUE
          nmax = nmax1
      else
          k = nmax1 * (nmax1 + 2)
          l = nmax2 * (nmax2 + 2)
C          for i = k + 1, l
      DO  1020  i = k + 1, l
            gh(i) = factor * gh2(i)
C          end for
 1020 CONTINUE
 1021 CONTINUE
          nmax = nmax2
      endif
 
C      for i = 1, k
      DO  1030  i = 1, k
          gh(i) = gh1(i) + factor * (gh2(i) - gh1(i))
C      end for
 1030 CONTINUE
 1031 CONTINUE
 
      return
      end
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ bfieldsr  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
      subroutine extrapshc (date, dte1, nmax1, gh1, nmax2,
     1                        gh2, nmax, gh)
 
c ===============================================================
c
c      version 1.01
c
c      extrapolates linearly a spherical harmonic model with a
c      rate-of-change model.
c
c      input:
c          date  - date of resulting model (in decimal year)
c          dte1  - date of base model
c          nmax1 - maximum degree and order of base model
c          gh1   - schmidt quasi-normal internal spherical
c                harmonic coefficients of base model
c          nmax2 - maximum degree and order of rate-of-change
c                model
c          gh2   - schmidt quasi-normal internal spherical
c                harmonic coefficients of rate-of-change model
c
c      output:
c          gh    - coefficients of resulting model
c          nmax  - maximum degree and order of resulting model
c
c      a. zunde
c      usgs, ms 964, box 25046 federal center, denver, co  80225
c
c ===============================================================
 
      dimension      gh1(*), gh2(*), gh(*)
 
c ---------------------------------------------------------------
c      the coefficients (gh) of the resulting model, at date
c      date, are computed by linearly extrapolating the coef-
c      ficients of the base model (gh1), at date dte1, using
c      those of the rate-of-change model (gh2), at date dte2. if
c      one model is smaller than the other, the extrapolation is
c      performed with the missing coefficients assumed to be 0.
c ---------------------------------------------------------------
 
      factor = (date - dte1)
 
      if (nmax1 .eq. nmax2) then
          k = nmax1 * (nmax1 + 2)
          nmax = nmax1
      else if (nmax1 .gt. nmax2) then
          k = nmax2 * (nmax2 + 2)
          l = nmax1 * (nmax1 + 2)
C          for i = k + 1, l
      DO  1010  i = k + 1, l
            gh(i) = gh1(i)
C          end for
 1010 CONTINUE
 1011 CONTINUE
          nmax = nmax1
      else
          k = nmax1 * (nmax1 + 2)
          l = nmax2 * (nmax2 + 2)
C          for i = k + 1, l
      DO  1020  i = k + 1, l
            gh(i) = factor * gh2(i)
C          end for
 1020 CONTINUE
 1021 CONTINUE
          nmax = nmax2
      endif
 
C      for i = 1, k
      DO  1030  i = 1, k
          gh(i) = gh1(i) + factor * gh2(i)
C      end for
 1030 CONTINUE
 1031 CONTINUE
 
      return
      end
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ bfieldsr  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
      subroutine shval3 (igdgc, flat, flon, elev, erad, a2, b2,
     1                     nmax, gh, iext, ext, x, y, z)
 
c ================================================================
c
c      version 1.01
c
c      calculates field components from spherical harmonic (sh)
c      models.
c
c      input:
c          igdgc - indicates coordinate system used; set equal to
c                1 if geodetic, 2 if geocentric
c          flat  - north latitude, in degrees
c          flon  - east longitude, in degrees
c          elev  - elevation above mean sea level (igdgc=1), or
c                radial distance from earth's center (igdgc=2)
c          erad  - value of earth's radius associated with the sh
c                coefficients, in same units as elev
c          a2,b2 - squares of semi-major and semi-minor axes of
c                the reference spheroid used for transforming
c                between geodetic and geocentric coordinates or
c                components
c          nmax  - maximum degree and order of coefficients
c          gh    - schmidt quasi-normal internal spherical
c                harmonic coefficients
c          iext  - external coefficients flag (= 0 if none)
c          ext   - the three 1st-degree external coefficients
c                (not used if iext = 0)
c
c      output:
c          x     -  northward component
c          y     -  eastward component
c          z     -  vertically-downward component
c
c      based on subroutine "igrf" by d. r. barraclough and
c      s. r. c. malin, report no. 71/1, institute of geological
c      sciences, u.k.
c
c      norman w. peddie, u.s. geological survey, mail stop 964,
c      federal center, box 25046, denver, colorado 80225
c
c ================================================================
 
c      the required sizes of the arrays used in this subroutine
c      depend on the value of nmax.  the minimum dimensions
c      needed are indicated in the table below.  (note that this
c      version is dimensioned for nmax of 14 or less).
c
c                                  minimum dimension
c                              --------------------------
c  nmax
      dimension  sl(14), cl(14)
c (nmax * (nmax + 3)) / 2
      dimension  p(119), q(119)
c  nmax * (nmax + 2)
      dimension  gh(224)
c  3
      dimension  ext(3)
 
c ================================================================
 
      parameter  (dtr = .01745329)

      r = elev
      slat = sin (flat * dtr)
      if (90. - flat .lt. .001) then
c 300 ft from n. pole
          aa = 89.999
      else if (90. + flat .lt. .001) then
c 300 ft from s. pole
          aa = -89.999
      else
          aa = flat
      endif
      clat = cos (aa * dtr)
      sl(1) = sin (flon * dtr)
      cl(1) = cos (flon * dtr)
      x = 0.
      y = 0.
      z = 0.
      sd = 0.
      cd = 1.
      n = 0
      l = 1
      m = 1
      npq = (nmax * (nmax + 3)) / 2
 
      if (igdgc .eq. 1) then
          aa = a2 * clat * clat
          bb = b2 * slat * slat
          cc = aa + bb
          dd = sqrt (cc)
          r = sqrt (elev * (elev + 2. * dd)
     1                   + (a2 * aa + b2 * bb) / cc)
          cd = (elev + dd) / r
          sd = (a2 - b2) / dd * slat * clat / r

          aa = slat
          slat = slat * cd - clat * sd
          clat = clat * cd + aa * sd
      endif
 
      ratio = erad / r
 
      aa = sqrt (3.)
      p(1) = 2. * slat
      p(2) = 2. * clat
      p(3) = 4.5 * slat * slat - 1.5
      p(4) = 3. * aa * clat * slat
      q(1) = -clat
      q(2) = slat
      q(3) = -3. * clat * slat
      q(4) = aa * (slat * slat - clat * clat)
 
C      for k = 1, npq
      DO  1010  k = 1, npq
          if (n .lt. m) then
            m = 0
            n = n + 1
            rr = ratio**(n + 2)
            fn = n
          endif
          fm = m
          if (k .ge. 5) then
            if (m .eq. n) then
                aa = sqrt (1. - .5 / fm)
                j = k - n - 1
                p(k) = (1. + 1. / fm) * aa * clat * p(j)
                q(k) = aa * (clat * q(j) + slat / fm * p(j))
                sl(m) = sl(m-1) * cl(1) + cl(m-1) * sl(1)
                cl(m) = cl(m-1) * cl(1) - sl(m-1) * sl(1)
            else
                aa = sqrt (fn * fn - fm * fm)
                bb = sqrt ((fn - 1.)**2 - fm * fm) / aa
                cc = (2. * fn - 1.) / aa
                i = k - n
                j = k - 2 * n + 1
                p(k) = (fn + 1.) * (cc * slat / fn * p(i) - bb
     1                       / (fn - 1.) * p(j))
                q(k) = cc * (slat * q(i) - clat / fn * p(i))
     1                     - bb * q(j)
            endif
          endif
 
          aa = rr * gh(l)

          if (m .eq. 0) then
            x = x + aa * q(k)
            z = z - aa * p(k)
            l = l + 1
          else
            bb = rr * gh(l+1)
            cc = aa * cl(m) + bb * sl(m)
            x = x + cc * q(k)
            z = z - cc * p(k)
            if (clat .gt. 0.) then
                y = y + (aa * sl(m) - bb * cl(m)) * fm * p(k)
     1                  / ((fn + 1.) * clat)
            else
                y = y + (aa * sl(m) - bb * cl(m)) * q(k)
     1                * slat
            endif
            l = l + 2
          endif
          m = m + 1
C      end for
 1010 CONTINUE
 1011 CONTINUE
 
      if (iext .ne. 0) then
          aa = ext(2) * cl(1) + ext(3) * sl(1)
          x = x - ext(1) * clat + aa * slat
          y = y + ext(2) * sl(1) - ext(3) * cl(1)
          z = z + ext(1) * slat + aa * clat
      endif
 
      aa = x
      x = x * cd + z * sd
      z = z * cd - aa * sd
 
      
      return
      end
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ bfieldsr  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
      subroutine dihf (x, y, z, d, i, h, f)
 
c ===============================================================
c
c      version 1.01
c
c      computes the geomagnetic elements d, i, h, and f from
c      x, y, and z.
c
c      input:
c          x   - northward component
c          y   - eastward component
c          z   - vertically-downward component
c
c      output:
c          d   - declination
c          i   - inclination
c          h   - horizontal intensity
c          f   - total intensity
c
c      a. zunde
c      usgs, ms 964, box 25046 federal center, denver, co  80225
c
c ===============================================================
 
      real            i
      parameter     ( sn = 0.0001 )
 
c ---------------------------------------------------------------
c      if d and i cannot be determined, set equal to 999.0.
c ---------------------------------------------------------------
 
      h2 = x*x + y*y
      h = sqrt (h2)
      f = sqrt (h2 + z*z)
      if (f .lt. sn) then
          d = 999.
          i = 999.
      else
          i = atan2 (z, h)
          if (h .lt. sn) then
            d = 999.
          else
            hpx = h + x
            if (hpx .lt. sn) then
                d = 180.
            else
                d = 2. * atan2 (y, hpx)
            endif
          endif
      endif
 
      return
      end
