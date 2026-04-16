(set-logic ALL)
; Constraint ID: 614a56de179850d2
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59851)) (False)
(assert (not (= x 59851)))

; Query: ((== x 59852)) (False)
(assert (not (not (= x 59852))))

(check-sat)
(get-model)
