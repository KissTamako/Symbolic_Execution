(set-logic ALL)
; Constraint ID: 1a00e050d71d1c7f
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60307)) (False)
(assert (not (= x 60307)))

; Query: ((== x 60308)) (False)
(assert (not (not (= x 60308))))

(check-sat)
(get-model)
