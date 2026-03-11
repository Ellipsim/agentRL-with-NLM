

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b9)
(on b2 b5)
(on-table b3)
(on-table b4)
(on-table b5)
(on b6 b7)
(on b7 b8)
(on b8 b3)
(on b9 b2)
(clear b1)
(clear b4)
(clear b6)
)
(:goal
(and
(on b2 b7)
(on b3 b4)
(on b7 b9)
(on b8 b2)
(on b9 b6))
)
)


