

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b10)
(on b2 b6)
(ontable b3)
(on b4 b11)
(ontable b5)
(on b6 b3)
(ontable b7)
(on b8 b5)
(on b9 b1)
(on b10 b7)
(on b11 b9)
(on b12 b4)
(clear b2)
(clear b8)
(clear b12)
)
(:goal
(and
(on b1 b11)
(on b2 b10)
(on b4 b9)
(on b5 b6)
(on b6 b12)
(on b9 b2)
(on b10 b8)
(on b12 b7))
)
)


