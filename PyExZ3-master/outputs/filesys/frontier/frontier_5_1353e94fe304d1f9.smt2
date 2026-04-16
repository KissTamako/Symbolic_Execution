(set-logic ALL)
; Constraint ID: 1353e94fe304d1f9
; Generated at: 2026-04-16 11:40:22
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60142)) (False)
(assert (not (= x 60142)))

; Query: ((== x 60143)) (False)
(assert (not (not (= x 60143))))

(check-sat)
(get-model)
