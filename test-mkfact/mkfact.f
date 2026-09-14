
      subroutine mkfact(tm,h,bfm,thb,bki,nhts)
c
c      create table of magnetic field components
c
      real h(nhts),bfm(nhts),thb(nhts),bki(nhts)
      data pio180/0.017453292/,pi/3.14159265/
C     rate of rotation produced by n=1 cm-3, b=1 gauss
      data rate/1.8978873e-6/
C     Jicamarca position
      data gdlat/-11.951/,elon/-76.8667/,gdalt/0./,re/6280.0/
C     3.0, 4.5, 6.0 and 3.38N degree positions 
c      data decd/-12.88/,ham/-4.617/
c      data decd/-13.1/,ham/-5.0/  ! made up
c     data decd/-14.56/,ham/-5.33/
c      data decd/-16.24/,ham/-6.03/
c      data decd/-9.52/,ham/-3.20/ ! Faraday DP classic
c      data decd/ -9.90/,ham/  3.23/ ! Faraday test 2025_11
c       data decd/ -9.90/,ham/  -3.23/ ! Faraday test 2025_11 2
       data decd/ -15.82/,ham/-6.13/ ! Valley 2026 08 
c=======
c
c     convert from geodetic to geocentric coordinates
c
      call convrt(1,gdlat,gdalt,gclat,re)
c
c     convert from degrees to radians
c
      gclat=gclat*pio180
      elong=elon*pio180
c
c     create components of vector from center of earth
c     to antenna center

      ca=cos(elong)
      cd=cos(gclat)
      sa=sin(elong)
      sd=sin(gclat)
      rx=re*ca*cd
      ry=re*sa*cd
      rz=re*sd
c
c     create antenna normal vector (unit vector in direction of k)
c
      dec=decd*pio180
      ha=ham*pi/720.+elong
      ch=cos(ha)
      sh=sin(ha)
      cdec=cos(dec)
      sdec=sin(dec)
      ax=ch*cdec
      ay=sh*cdec
      az=sdec
      do i=1,nhts
c
c       create vector from center of earth to scattering volume
c
        x=rx+ax*h(i)
        y=ry+ay*h(i)
        z=rz+az*h(i)
        x2y2=x*x+y*y
        r=sqrt(x2y2+z*z)
        x2y2=sqrt(x2y2)
c
c       convert to spherical coordinates
c
        st=x2y2/r
        ct=z/r
        sp=y/x2y2
        cp=x/x2y2
c       call milmag(tm,r,st,ct,sp,cp,br,bt,bp,b)
        theta=atan2(st,ct)
        phi=atan2(sp,cp)
        call geobfield(tm,r,theta,phi,br,bt,bp,b)

c
c       convert to cartesian coordinates
c
        bx=br*st*cp+bt*ct*cp-bp*sp
        by=br*st*sp+bt*ct*sp+bp*cp
        bz=br*ct-bt*st
        bk=(ax*bx+ay*by+az*bz)
        thb(i)=acos(abs(bk/b))*57.29577951
        bfm(i)=b
        bki(i)=1.0/bk

      end do
      return
      end

      subroutine gausfit(drift,hist,vz,m)
c
c     fit procedure for estimating velocities
c
      real drift(m),hist(m),vz
      real x(1000),y(1000)
      parameter(n=6)
      real a(n),tol,wa(m*n+5*n+m),wa2(m*n+5*n+m),fvec(m)
      integer info,iwa(n),lwa
      external gauss
      common/gf/x,y
      data vlast/0.0/

      lwa=m*n+5*n+m
      tol=1.0e-6
      info=0
      amax=0.0

      do i=1,m
         x(i)=drift(i)
         y(i)=hist(i)
         amax=max(amax,hist(i))
      end do

      a(1)=amax
      a(2)=-20.0
      a(3)=20.0

      a(4)=amax/4.0
      a(5)=20.0
      a(6)=20.0

c      write(*,*) m,n,a,tol,info

      call lmdif1(gauss,m,n,a,fvec,tol,info,iwa,wa,lwa)
     
      call fdjac2(gauss,m,n,a,fvec,wa,m,iflag,0.0e0,wa2)
      if(abs(a(1)).gt.abs(a(4))) then
         vz=a(2)
         i=2
      else
         vz=a(5)
         i=5
      end if

      err=0.0
      do j=1,m
         err=err+(wa(j+(i-1)*m))**2
      end do
      if(err.gt.0.0) err=sqrt(err**-1)
      
c
c     try fitting single distribution
c
      a(1)=amax
      a(2)=-20.0
      a(3)=20.0

      call lmdif1(gauss,m,n/2,a,fvec,tol,info,iwa,wa,lwa)
      call fdjac2(gauss,m,n/2,a,fvec,wa,m,iflag,0.0e0,wa2)
      vz1=a(2)
      i=2

      err1=0.0
      do j=1,m
         err1=err1+(wa(j+(i-1)*m))**2
      end do
      if(err1.gt.0.0) err1=sqrt(err**-1)


      if(err1.lt.err.or.abs(vz-vz1).lt.10.0) vz=vz1
      vz=vz1
      vlast=vz

      return
      end

      subroutine gauss(m,n,a,fvec,iflag)
c
      integer m,n,iflac
      real fvec(m),a(n),b
      real x(1000),y(1000)
      common/gf/x,y
c
      
      do i=1,m
         sig=sqrt(max(1.0,y(i)))
         b=abs(a(1))*exp(-(a(2)-x(i))**2/(2.0*a(3)**2))
         if(n.gt.3) then
            c=abs(a(4))*exp(-(a(5)-x(i))**2/(2.0*a(6)**2))
         else
            c=0.0
         end if
         fvec(i)=(b+c-y(i))**2/sig**2
      end do
      return
      end
         




