;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-intermediate-lambda-reader.ss" "lang")((modname ConvertFile) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))


;; a FileFormat is (anyof 'x 'y 'z)

(define-struct file (size format))
;; a File is a (make-file Nat FileFormat)
;; requires:
;;     format represents the file format (similar to .jpg or .rkt
;;       in a real computer)
;;     size represents how much space it uses on the computer

(define-struct folder (files subfolders))
;; a Folder is a (make-folder (listof File) (listof Folder))
;; requires:
;;      files represents all of the files directly in this folder
;;      subfolders represents the folders directly in this folder

(define f10x (make-file 10 'x))
(define f25y (make-file 25 'y))
(define f30x (make-file 30 'x))
(define f25x (make-file 25 'x))
(define f10y (make-file 10 'y))
(define f10z (make-file 10 'z))
(define f30x-copy (make-file 30 'x))
(define f10z-copy (make-file 10 'z))
(define f50y (make-file 50 'y))
(define f30z (make-file 30 'z))
(define f0x (make-file 0 'x))
(define f50z (make-file 50 'z))
(define fldA (make-folder (list f10x f25y f30z) empty))
(define fldB (make-folder (list f25x f30x-copy) empty))
(define fldC (make-folder (list f10z f10y f50y) empty))
(define fldD (make-folder (list f10z-copy f30x) (list fldA)))
(define fldE (make-folder empty (list fldB fldC)))
(define fldF (make-folder (list f0x f50z) (list fldD fldE)))

;; (convert old-fft new-fft fld) produces a Folder that each
;; old format type old-fft is replaced by the new format type
;; new-fft in a Folder fld
;; convert: File-Format File-Format Folder -> Folder
;; Examples:
(check-expect (convert 'x 'y fldA) (make-folder (list (make-file 10 'y)
                                                      (make-file 25 'y)
                                                      (make-file 30 'z))
                                                empty ))
(check-expect (convert 'x 'z fldA) (make-folder (list (make-file 10 'z)
                                                      (make-file 25 'y)
                                                      (make-file 30 'z))
                                                empty ))


(define (convert old-fft new-fft fld)
  (local
    [;; (replace-fft files) produces a list of files
     ;;  in which all old formats old-fft are replaced
     ;;  by new formats new-fft.
     ;; replace-fft: (listof File) -> (listof File)
     (define (replace-fft files)
       (cond
         [(empty? files) empty]
         [(equal? old-fft (file-format (first files)))
          (cons
           (make-file (file-size (first files)) new-fft)
           (replace-fft (rest files)))]
         [else (cons
                (first files)
                (replace-fft (rest files)))]))
     ;; (replace-fft-fld alof) produces a list of folders
     ;;  in which all old formats old-fft are replaced
     ;;  by new formats new-fft.
     ;; replace-fft-fld: (listof Folder) -> (listof Folder)
     (define (replace-fft-fld alof)
       (cond
         [(empty? alof) empty]
         [else (cons
                (convert old-fft new-fft (first alof))
                (replace-fft-fld (rest alof)))]))]
 (make-folder (replace-fft (folder-files fld))
              (replace-fft-fld (folder-subfolders fld)))))

;;Tests:
(check-expect (convert 'x 'z fldA)
              (make-folder (list
                            (make-file 10 'z)
                            (make-file 25 'y)
                            (make-file 30 'z))
                           empty))
(check-expect (convert 'y 'y fldF) fldF)
(check-expect (convert 'x 'y fldE)
              (make-folder empty
                           (list
                            (make-folder (list (make-file 25 'y)
                                               (make-file 30 'y))
                                         empty)
                            (make-folder (list (make-file 10 'z)
                                               (make-file 10 'y)
                                               (make-file 50 'y))
                                         empty))))
(check-expect (convert 'x 'y fldB)
               (make-folder (list (make-file 25 'y)
                                  (make-file 30 'y))
                            empty))
(check-expect (convert 'z 'y fldC)
               (make-folder (list (make-file 10 'y)
                                  (make-file 10 'y)
                                  (make-file 50 'y))
                            empty))
(check-expect (convert 'x 'z fldD)
               (make-folder (list (make-file 10 'z)
                                  (make-file 30 'z))
                            (list
                                  (make-folder
                            (list
                                  (make-file 10 'z)
                                  (make-file 25 'y)
                                  (make-file 30 'z))
                            empty))))
                              

                               