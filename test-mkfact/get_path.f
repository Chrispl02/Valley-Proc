
      subroutine get_path(fqual_temp)
c
c      create table of magnetic field components
c
c      character*47 L

      character(1024) :: fqual_temp
      character(512) :: ppath
      character(512) :: cpath
      ppath = "/home/david/Documents/faraday-experiment/schain"
      cpath = "/schainf/Ffiles/bfmodel/"    
c      write(*,*) "Len:", L
      fqual_temp = TRIM(ppath)//TRIM(cpath)
c      write(*,*) "Len:", fqual_temp
      return
      end
