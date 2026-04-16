(set-logic ALL)
; Constraint ID: bf28cc87a7bd36a6
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60451)) (False)
(assert (not (= x 60451)))

; Query: ((== x 60452)) (False)
(assert (not (not (= x 60452))))

(check-sat)
(get-model)
