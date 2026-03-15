

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b5)
(on b2 b9)
(on b3 b2)
(on b4 b1)
(on-table b5)
(on b6 b7)
(on b7 b4)
(on-table b8)
(on b9 b6)
(clear b3)
(clear b8)
)
(:goal
(and
(on b1 b7)
(on b2 b8)
(on b4 b3)
(on b7 b5))
)
)


