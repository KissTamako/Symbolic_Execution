(set-logic ALL)
; Constraint ID: fdb9758ed3e135f2
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60088)) (False)
(assert (not (= x 60088)))

; Query: ((== x 60089)) (False)
(assert (not (not (= x 60089))))

(check-sat)
(get-model)
