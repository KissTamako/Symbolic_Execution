(set-logic ALL)
; Constraint ID: 954d1272e6966c0e
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60310)) (False)
(assert (not (= x 60310)))

; Query: ((== x 60311)) (False)
(assert (not (not (= x 60311))))

(check-sat)
(get-model)
