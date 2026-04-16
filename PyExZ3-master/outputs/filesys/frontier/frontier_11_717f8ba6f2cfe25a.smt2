(set-logic ALL)
; Constraint ID: 717f8ba6f2cfe25a
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59476)) (False)
(assert (not (= x 59476)))

; Query: ((== x 59477)) (False)
(assert (not (not (= x 59477))))

(check-sat)
(get-model)
