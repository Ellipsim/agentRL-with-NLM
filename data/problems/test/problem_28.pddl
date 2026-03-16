

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b9)
(on b2 b7)
(on b3 b4)
(on b4 b6)
(ontable b5)
(on b6 b5)
(on b7 b1)
(ontable b8)
(on b9 b3)
(on b10 b2)
(clear b8)
(clear b10)
)
(:goal
(and
(on b1 b5)
(on b3 b8)
(on b4 b9)
(on b5 b4)
(on b6 b1)
(on b7 b2)
(on b8 b7)
(on b9 b10))
)
)


