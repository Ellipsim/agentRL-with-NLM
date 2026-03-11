

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on-table b1)
(on b2 b8)
(on b3 b9)
(on b4 b2)
(on b5 b1)
(on b6 b4)
(on b7 b6)
(on-table b8)
(on-table b9)
(clear b3)
(clear b5)
(clear b7)
)
(:goal
(and
(on b1 b5)
(on b2 b9)
(on b4 b7)
(on b5 b3)
(on b6 b2))
)
)


