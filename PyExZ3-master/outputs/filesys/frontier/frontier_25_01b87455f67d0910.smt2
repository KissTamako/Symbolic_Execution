(set-logic ALL)
; Constraint ID: 01b87455f67d0910
; Generated at: 2026-04-16 11:42:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60247)) (False)
(assert (not (= x 60247)))

; Query: ((== x 60248)) (False)
(assert (not (not (= x 60248))))

(check-sat)
(get-model)
