

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b7)
(on-table b2)
(on b3 b6)
(on b4 b5)
(on-table b5)
(on b6 b4)
(on-table b7)
(on b8 b2)
(on b9 b8)
(clear b1)
(clear b3)
(clear b9)
)
(:goal
(and
(on b1 b3)
(on b3 b7)
(on b4 b8)
(on b6 b5)
(on b7 b2)
(on b8 b6)
(on b9 b1))
)
)


