(set-logic ALL)
; Path ID: 490a9005e62f6577
; Generated at: 2026-04-16 12:01:21
; Solver: Z3Wrapper
; Number of assertions: 2
; Has query: True

(declare-const a Int)
(declare-const b Int)
(declare-const se Int)

; ((== (+ (- (* (* 2 b) b) (* 5 b)) 3) 0)) (True)
(assert (= (+ (- (* (* 2 b) b) (* 5 b)) 3) 0))
; ((== (+ (- (* (* 2 a) a) (* 5 a)) 3) 0)) (True)
(assert (= (+ (- (* (* 2 a) a) (* 5 a)) 3) 0))

; Query: ((!= a b)) (False)
(assert (not (not (not (= a b)))))

(check-sat)
(get-model)
