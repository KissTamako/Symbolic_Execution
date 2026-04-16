(set-logic ALL)
; Executed Path ID: 5f98cd769c640128
; Generated at: 2026-04-17 03:12:45
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: False

(declare-const c Int)

; ((== (+ 3 c) 6)) (False)
(assert (not (= (+ 3 c) 6)))

(check-sat)
(get-model)
