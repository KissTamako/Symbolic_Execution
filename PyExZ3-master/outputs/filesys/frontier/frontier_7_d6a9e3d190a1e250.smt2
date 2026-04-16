(set-logic ALL)
; Constraint ID: d6a9e3d190a1e250
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60595)) (False)
(assert (not (= x 60595)))

; Query: ((== x 60596)) (False)
(assert (not (not (= x 60596))))

(check-sat)
(get-model)
