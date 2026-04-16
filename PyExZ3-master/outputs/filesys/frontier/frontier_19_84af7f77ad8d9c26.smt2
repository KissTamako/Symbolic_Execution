(set-logic ALL)
; Constraint ID: 84af7f77ad8d9c26
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59488)) (False)
(assert (not (= x 59488)))

; Query: ((== x 59489)) (False)
(assert (not (not (= x 59489))))

(check-sat)
(get-model)
