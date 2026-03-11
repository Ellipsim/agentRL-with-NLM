

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b4)
(on b2 b7)
(on-table b3)
(on-table b4)
(on b5 b9)
(on-table b6)
(on-table b7)
(on b8 b6)
(on b9 b8)
(on b10 b3)
(clear b1)
(clear b2)
(clear b5)
(clear b10)
)
(:goal
(and
(on b1 b2)
(on b2 b8)
(on b3 b7)
(on b5 b1)
(on b6 b9)
(on b8 b6)
(on b9 b4)
(on b10 b5))
)
)


