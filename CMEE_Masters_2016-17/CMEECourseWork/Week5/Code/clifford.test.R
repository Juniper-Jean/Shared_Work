clifford.test <- function(A, B, ew.wrap=FALSE){
    
    A.nm <- deparse(substitute(A))
    B.nm <- deparse(substitute(B))
    
    # do some double checking
    if(! all(dim(A) == dim(B))) stop("Matrices must have same dimensions")
    if(! all(is.na(A) == is.na(B))) {
        warning("Non-identical missing values: using pairwise complete")
        union.na <- is.na(A) | is.na(B)
        A[union.na] <- NA
        B[union.na] <- NA
    }
    
    # alleged sample size
    n <- sum(!is.na(A))
    
    # centre the matrices around 0
    A <- A - mean(A, na.rm=TRUE)
    B <- B - mean(B, na.rm=TRUE)
    
    # get the variance estimates
    sv.A <- var(as.vector(A),na.rm=TRUE)
    sv.B <- var(as.vector(B), na.rm=TRUE)
    
    # get the pearson correlation 
    rpearson <- cor(as.vector(A), as.vector(B), use="p", method="pearson")
    
    # get the autocorrelation estimates from the matrices
    acf.A <- clifford.acf(A, ew.wrap=ew.wrap)
    acf.B <- clifford.acf(B, ew.wrap=ew.wrap)
    
    
    if(all(acf.A$nok != acf.B$nok)) stop("Unexpectedly non-matching N(k)") # paranoia

    ncc <- sum(acf.A$nok*acf.A$acf*acf.B$acf)
    
    var.xy <- ncc/n^2
    if(var.xy <= 0) var.xy = (sv.A*sv.B)/n # see Richardson et al (1989)
    
    var.r <- var.xy/(sv.A*sv.B)
    ess <- 1+1/var.r
    w <- rpearson*((ess-1)^0.5)
    t <- rpearson*(sqrt((ess-2)/(1-rpearson)))
    p <- 1-pt(t, ess-2)

    RET <- list(A=list(name=A.nm, mat=A, acf=acf.A$acf, svar=sv.A), 
                B=list(name=B.nm, mat=B, acf=acf.B$acf, svar=sv.B),
                nok=acf.A$nok, rpearson=rpearson, n=n, ncc=ncc, 
                var.xy=var.xy, var.r=var.r, ess=ess, w=w, t=t,p=p)
                
    class(RET) <- "clifford.test"
    return(RET)    
}

clifford.acf <- function(x, ew.wrap=FALSE){

    # This is slow by comparison to the Fortran version:
    # ~ 45 minutes for a 360x152 matrix as compared to ~ 7 minutes

    # get the dimensions and the output matrices
    nr <- dim(x)[1]
    nc <- dim(x)[2]
    nok <- acf <- matrix(0, ncol=(nc*2)-1, nrow=(nr*2)-1)
        
    # create a 0/1 matrix showing non-NA values
    not.na.x <- !(is.na(x))
    # and a copy with NA set to zero to avoid n+NA -> 0
    xx <- x
    xx[is.na(xx)] <- 0
    
	# sum the products of each cell against each lag...
	for(r in 1:nr){
		for(c in 1:nc){
			#  ... as long as the cell isn't NA
			if(!is.na(x[r,c])){
				indr <- ((nr + 1) - r):(((nr + 1) - r) + (nr - 1))
				indc <- ((nc + 1) - c):(((nc + 1) - c) + (nc - 1))
				acf[indr,indc] <- acf[indr, indc] + (xx*xx[r,c])
				nok[indr,indc] <- nok[indr, indc] + not.na.x           
			}
		}
	}   
    
    if(ew.wrap){
    	
    	acf.nc <- ((nc*2)-1) 

		# find the number of columns to wrap from each side
        # arbitrarily breaking even numbers of columns
        cols.to.wrap <- acf.nc - nc
        left.wrap <- ceiling(cols.to.wrap/2) 
        right.wrap <- floor(cols.to.wrap/2)
        
        # calculate vectors of the old and new positions
        lo <- 1:left.wrap
        ro <- (acf.nc - right.wrap + 1):acf.nc
        ln <- (acf.nc - right.wrap + 1 - left.wrap):(acf.nc - right.wrap)
        rn <- (left.wrap + 1):(left.wrap + right.wrap)
        
        acf[,rn] <- acf[,rn] + acf[,ro]
		acf[,ln] <- acf[,ln] + acf[,lo]
		acf[,lo] <- 0
		acf[,ro] <- 0
		
        nok[,rn] <- nok[,rn] + nok[,ro]
		nok[,ln] <- nok[,ln] + nok[,lo]
		nok[,lo] <- 0
		nok[,ro] <- 0

       
    }
    
    acf <- acf/nok
    
    # need to allow for lags that have no representations in
    # the dataset - the averaging above will do 0/0 and hence NaN
    acf[is.nan(acf)]  <- 0
    
    return(list(acf=acf, nok=nok))
}

print.clifford.test <- function(x, ...){

	cat("\nCorrelation test accounting for autocorrelation (Clifford et al., 1989)\n\nData - Matrix A:", x$A$name, 
	    "\n     - Matrix B:", x$B$name, "\n\n")
	print(as.data.frame(x[4:12], row.names=""))
	cat("\n")
}

