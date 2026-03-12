

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b8)
(on b2 b5)
(on-table b3)
(on-table b4)
(on b5 b9)
(on b6 b4)
(on b7 b1)
(on b8 b3)
(on b9 b7)
(clear b2)
(clear b6)
)
(:goal
(and
(on b2 b3)
(on b3 b4)
(on b4 b6)
(on b5 b8)
(on b6 b9)
(on b7 b2)
(on b9 b1))
)
)


