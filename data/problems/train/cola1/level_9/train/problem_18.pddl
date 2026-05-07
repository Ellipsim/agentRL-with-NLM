

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(on b3 b4)
(on b4 b2)
(ontable b5)
(on b6 b5)
(on b7 b9)
(on b8 b3)
(ontable b9)
(on b10 b6)
(clear b7)
(clear b8)
(clear b10)
)
(:goal
(and
(on b1 b8)
(on b2 b6)
(on b6 b4)
(on b7 b10)
(on b8 b3)
(on b9 b1)
(on b10 b5))
)
)


