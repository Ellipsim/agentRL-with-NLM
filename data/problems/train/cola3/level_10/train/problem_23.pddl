

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b10)
(on b2 b8)
(on b3 b9)
(ontable b4)
(ontable b5)
(on b6 b3)
(ontable b7)
(on b8 b4)
(on b9 b1)
(on b10 b12)
(on b11 b2)
(on b12 b11)
(clear b5)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b11)
(on b3 b9)
(on b4 b12)
(on b5 b8)
(on b6 b3)
(on b7 b5)
(on b8 b10)
(on b10 b6)
(on b12 b1))
)
)


