(set-logic ALL)
; Executed Path ID: cf950aada34d7026
; Generated at: 2026-04-16 16:02:50
; Solver: Z3Wrapper
; Number of predicates: 3
; Has query: False

(declare-const a Int)
(declare-const b Int)

; ((== (+ (- (* (* 2 a) a) (* 5 a)) 3) 0)) (True)
(assert (= (+ (- (* (* 2 a) a) (* 5 a)) 3) 0))
; ((== (+ (- (* (* 2 b) b) (* 5 b)) 3) 0)) (True)
(assert (= (+ (- (* (* 2 b) b) (* 5 b)) 3) 0))
; ((!= a b)) (False)
(assert (not (not (= a b))))

(check-sat)
(get-model)
