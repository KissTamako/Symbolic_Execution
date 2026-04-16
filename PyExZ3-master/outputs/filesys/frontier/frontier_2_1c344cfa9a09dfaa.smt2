(set-logic ALL)
; Constraint ID: 1c344cfa9a09dfaa
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60514)) (False)
(assert (not (not (= x 60514))))

(check-sat)
(get-model)
